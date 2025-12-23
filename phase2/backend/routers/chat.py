"""
Chat Router for AI-powered task management using OpenRouter

Uses OpenRouter API (OpenAI-compatible) with MCP tools for function calling.
"""

import os
import json
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
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
    user_id: str,
    request: ChatRequest,
    db: Session = Depends(get_session)
):
    """
    AI-powered chat with task management capabilities using OpenRouter
    """
    try:
        print(f"\n💬 Chat request from {user_id}: {request.message}")
        
        # Build messages with history
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful task management assistant. "
                    "Help users manage their to-do list efficiently. "
                    "When users ask to add, list, update, or delete tasks, use the available tools. "
                    "Be friendly and concise in your responses."
                )
            }
        ]
        
        # Add conversation history if provided
        if request.conversation_history:
            messages.extend(request.conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": request.message})
        
        print(f"🔧 Calling OpenRouter with {len(messages)} messages...")
        
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
                
                # Execute via MCP server
                result = await mcp.execute_tool(
                    function_name,
                    function_args,
                    user_id
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
                model="openai/gpt-3.5-turbo",
                messages=messages,
                temperature=0.7
            )
            
            final_message = second_response.choices[0].message.content
        else:
            # No tool calls, use direct response
            final_message = response_message.content
        
        print(f"✅ AI Response: {final_message[:100]}...")
        
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
