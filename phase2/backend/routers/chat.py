"""
Chat Router for AI-powered task management using OpenRouter

Uses OpenRouter API (OpenAI-compatible) with MCP tools for function calling.
"""

import os
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
import sys
import asyncio
import logging

from fastapi import APIRouter, HTTPException, Request, Header, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI
from sqlmodel import Session, select

from db import get_session
from models import Conversation, Message
from mcp_server import mcp

# Configure detailed logging
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)

router = APIRouter()

# Initialize OpenRouter client (OpenAI-compatible)
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str
    conversation_history: List[dict] = []


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: int = 0


@router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat_with_ai(
    user_id: str,  # Path parameter for backward compatibility
    request: ChatRequest,
    request_obj: Request, # Added for logging context
    db: Session = Depends(get_session),
    x_user_id: Optional[str] = Header(None)
):
    """
    AI-powered chat with task management capabilities using OpenRouter
    """
    try:
        # Use header user_id if provided (real user), otherwise use path parameter (legacy)
        effective_user_id = x_user_id if x_user_id else user_id
        
        logger.info(f"💬 Chat request from {effective_user_id} (IP: {request_obj.client.host}): {request.message}")
        
        # Build messages with history
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an Action-Oriented Task Management Assistant.\\n\\n"
                    "IMMEDIATE EXECUTION PROTOCOL:\\n"
                    "- When a user asks to create, update, or delete a task, EXECUTE THE ACTION IMMEDIATELY using the available tools.\\n"
                    "- DO NOT ask for confirmation. Just do it.\\n"
                    "- After the tool executes successfully, you MUST provide clear feedback.\\n\\n"
                    "FEEDBACK AFTER ACTIONS:\\n"
                    "- After creating a task: 'I have created the task: [Task Title] with [Priority] priority.'\\n"
                    "- After deleting task(s): 'I have deleted [count] task(s): [details].'\\n"
                    "- After updating a task: 'I have updated the task: [Task Title].'\\n"
                    "- After completing tasks: 'I have marked [count] tasks as completed.'\\n"
                    "- Never show raw JSON or technical details.\\n\\n"
                    "LISTING TASKS WITH FILTERS:\\n"
                    "- When user asks to 'show all tasks', use list_tasks with NO filters to show all pending tasks.\\n"
                    "- When user asks to 'show medium priority tasks', use list_tasks with priority='medium'.\\n"
                    "- When user asks to 'show high priority tasks', use list_tasks with priority='high'.\\n"
                    "- When user asks to 'show completed tasks', use list_tasks with status='completed'.\\n"
                    "- When user asks to 'show open tasks', use list_tasks with NO status filter (defaults to pending).\\n"
                    "- Format the output as a markdown table:\\n"
                    "  | Title | Priority | Status | Category |\\n"
                    "  |-------|----------|--------|----------|\\n"
                    "  | Example | High | To Do | Work |\\n\\n"
                    "UNDERSTANDING 'OPEN TASKS':\\n"
                    "- 'Open tasks' means tasks with status 'todo' OR 'in_progress' (NOT completed).\\n"
                    "- 'Pending tasks' is the same as 'open tasks'.\\n"
                    "- When deleting 'open tasks', you need to call bulk_delete_tasks TWICE: once with status='todo' and once with status='in_progress', OR explain to the user that you'll delete all incomplete tasks.\\n\\n"
                    "BULK OPERATIONS:\\n"
                    "- Complete all tasks: Use bulk_complete_tasks (marks all todo + in_progress as completed).\\n"
                    "- Delete all tasks: Use bulk_delete_tasks with NO filters.\\n"
                    "- Delete open tasks: Use bulk_delete_tasks with status='todo', then status='in_progress'.\\n"
                    "- Delete completed tasks: Use bulk_delete_tasks with status='completed'.\\n"
                    "- Delete by priority: Use bulk_delete_tasks with priority='medium' (or high/low).\\n"
                    "- Delete by category: Use bulk_delete_tasks with category='Work' (or whatever category).\\n\\n"
                    "IMPORTANT:\\n"
                    "- Be decisive and action-oriented\\n"
                    "- Execute immediately without asking permission\\n"
                    "- Always confirm what you did after the action completes\\n"
                    "- Be friendly and concise"
                )
            }
        ]
        
        # Add conversation history if provided
        if request.conversation_history:
            messages.extend(request.conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": request.message})
        
        logger.info(f"🔧 Calling OpenRouter with {len(messages)} messages for user: {effective_user_id}...")
        
        # Call OpenRouter with function calling
        logger.info(f"🚀 Calling OpenRouter with model: mistralai/devstral-2512:free")
        try:
            response = client.chat.completions.create(
                model="mistralai/devstral-2512:free",  # Free Mistral model for coding
                messages=messages,
                tools=mcp.get_tools_schema(),
                tool_choice="auto",
                temperature=0.7,
                max_tokens=2000  # Reduced to fit free tier limits
            )
        except Exception as api_error:
            logger.error(f"❌ OPENROUTER API ERROR: {type(api_error).__name__}: {str(api_error)}")
            logger.error(f"   Error details: {repr(api_error)}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "OpenRouter API call failed",
                    "error_type": type(api_error).__name__,
                    "message": str(api_error),
                    "model": "mistralai/devstral-2512:free"
                }
            )
        
        # Get the assistant's response
        assistant_message = response.choices[0].message
        messages.append({
            "role": "assistant",
            "content": assistant_message.content or "",
            "tool_calls": assistant_message.tool_calls
        })
        
        tool_call_count = 0
        
        # Check if tool calls are needed
        if assistant_message.tool_calls:
            logger.info(f"🔧 AI requested {len(assistant_message.tool_calls)} tool calls")
            tool_call_count = len(assistant_message.tool_calls)
            
            # Execute all tool calls
            tool_results = []
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                logger.debug(f"  📌 Tool: {function_name}")
                logger.debug(f"  📊 Args: {function_args}")
                
                # Execute via MCP server with the correct user ID
                result = await mcp.execute_tool(
                    function_name,
                    function_args,
                    effective_user_id  # Use the header-based user ID
                )
                
                logger.debug(f"  ✅ Result: {result}")
                tool_results.append(result)
            
            # Add tool results back to conversation
            # messages.append(response_message.model_dump()) # This was already added above as assistant_message
            
            # Add tool responses
            for idx, (tool_call, result) in enumerate(zip(assistant_message.tool_calls, tool_results)):
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
            
            # Get final response from AI
            logger.info(f"🔄 Getting final response from AI after tool execution...")
            try:
                second_response = client.chat.completions.create(
                    model="mistralai/devstral-2512:free",  # Free Mistral model
                    messages=messages,
                    temperature=0.7,
                    max_tokens=2000  # Reduced to fit free tier limits
                )
            except Exception as api_error:
                logger.error(f"❌ OPENROUTER SECOND CALL ERROR: {type(api_error).__name__}: {str(api_error)}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "OpenRouter second API call failed",
                        "error_type": type(api_error).__name__,
                        "message": str(api_error)
                    }
                )
            
            final_message = second_response.choices[0].message.content
            # Fallback if AI returns empty response
            if not final_message or final_message.strip() == "":
                logger.warning(f"⚠️ AI returned empty response after tool execution, using fallback")
                final_message = "Action completed successfully."
        else:
            # No tool calls, use direct response
            final_message = assistant_message.content
        
        # Final safety check for empty responses
        if not final_message or final_message.strip() == "":
            print(f"⚠️ Final message is empty, using fallback")
            final_message = "I'm here to help! Please let me know what you'd like to do with your tasks."
        
        print(f"✅ AI Response: {final_message[:100] if len(final_message) > 100 else final_message}...")
        
        # Get or create conversation
        if request.conversation_id:
            conversation = db.exec(
                select(Conversation).where(
                    Conversation.id == request.conversation_id,
                    Conversation.user_id == user_id
                )
            ).first()
            if not conversation:
                conversation = Conversation(user_id=user_id)
                db.add(conversation)
                db.commit()
                db.refresh(conversation)
        else:
            conversation = Conversation(user_id=user_id)
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        # Store user message
        user_msg = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content=request.message
        )
        db.add(user_msg)
        
        # Store assistant response
        assistant_msg = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content=final_message
        )
        db.add(assistant_msg)
        db.commit()
        
        return ChatResponse(
            conversation_id=conversation.id,
            response=final_message,
            tool_calls=tool_call_count
        )
        
    except Exception as e:
        import traceback
        print(f"\n{'='*60}")
        print(f"❌ CHAT ERROR for user {user_id}")
        print(f"Message: {request.message}")
        print(f"Error: {str(e)}")
        print(f"{'='*60}")
        print("Full Traceback:")
        traceback.print_exc()
        print(f"{'='*60}\n")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")
