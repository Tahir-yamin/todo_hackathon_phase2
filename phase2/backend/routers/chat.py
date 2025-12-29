"""
Chat Router for AI-powered task management using OpenRouter

Uses OpenRouter API (OpenAI-compatible) with MCP tools for function calling.
"""

import os
import json
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session, select
from pydantic import BaseModel
from openai import OpenAI

from db import get_session
from models import Conversation, Message
from mcp_server import mcp

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
    db: Session = Depends(get_session),
    x_user_id: Optional[str] = Header(None)
):
    """
    AI-powered chat with task management capabilities using OpenRouter
    """
    try:
        # Use header user_id if provided (real user), otherwise use path parameter (legacy)
        effective_user_id = x_user_id if x_user_id else user_id
        
        print(f"\n💬 Chat request from {effective_user_id}: {request.message}")
        
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
                    "- After deleting a task: 'I have deleted the task: [Task Title].'\\n"
                    "- After updating a task: 'I have updated the task: [Task Title].'\\n"
                    "- After completing all tasks: 'I have marked [count] tasks as completed.'\\n"
                    "- Never show raw JSON or technical details.\\n\\n"
                    "LISTING TASKS:\\n"
                    "- When listing tasks, format the output as a markdown table:\\n"
                    "  | Title | Priority | Status | Category |\\n"
                    "  |-------|----------|--------|----------|\\n"
                    "  | Example | High | To Do | Work |\\n\\n"
                    "BULK OPERATIONS:\\n"
                    "- If the user says 'complete all tasks' or 'mark everything as done', use the bulk_complete_tasks tool.\\n"
                    "- If the user says 'delete all tasks', politely explain: 'I can delete specific tasks by ID, but I don\\'t have a bulk delete function yet. Which task would you like me to delete?'\\n\\n"
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
        
        print(f"🔧 Calling OpenRouter with {len(messages)} messages for user: {effective_user_id}...")
        
        # Call OpenRouter with function calling
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",  # Cost-effective model
            messages=messages,
            tools=mcp.get_tools_schema(),
            tool_choice="auto",
            temperature=0.7
        )
        
        response_message = response.choices[0].message
        tool_call_count = 0
        
        # Check if tool calls are needed
        if response_message.tool_calls:
            print(f"🔧 AI requested {len(response_message.tool_calls)} tool calls")
            tool_call_count = len(response_message.tool_calls)
            
            # Execute all tool calls
            tool_results = []
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"  📌 Tool: {function_name}")
                print(f"  📊 Args: {function_args}")
                
                # Execute via MCP server with the correct user ID
                result = await mcp.execute_tool(
                    function_name,
                    function_args,
                    effective_user_id  # Use the header-based user ID
                )
                
                print(f"  ✅ Result: {result}")
                tool_results.append(result)
            
            # Add tool results back to conversation
            messages.append(response_message.model_dump())
            
            # Add tool responses
            for idx, (tool_call, result) in enumerate(zip(response_message.tool_calls, tool_results)):
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
            
            # Get final response from AI
            print(f"🔄 Getting final response from AI...")
            second_response = client.chat.completions.create(
                model=os.getenv("AI_MODEL", "deepseek/deepseek-chat"),
                messages=messages,
                temperature=0.7
            )
            
            final_message = second_response.choices[0].message.content
            # Fallback if AI returns empty response
            if not final_message or final_message.strip() == "":
                print(f"⚠️ AI returned empty response after tool execution, using fallback")
                final_message = "Action completed successfully."
        else:
            # No tool calls, use direct response
            final_message = response_message.content
        
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
