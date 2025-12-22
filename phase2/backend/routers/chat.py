"""
Chat Router for AI-powered task management using Google Gemini

Simplified version using gemini_agent.py with automatic function calling.
"""

import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel

from backend.db import get_session
from backend.models import Conversation, Message

router = APIRouter()


class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    function_calls: list[dict] = []


@router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    db: Session = Depends(get_session)
):
    """
    Stateless chat endpoint using Google Gemini with automatic function calling
    """
    from backend.gemini_agent import run_agent
    
    try:
        print(f"\n💬 Chat request from {user_id}: {request.message}")
        
        # Call the simplified Gemini agent
        response_text = await run_agent(user_id, request.message, db)
        
        # Get or create conversation for tracking
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
            user_id=user_id,  # CRITICAL FIX: Use path parameter
            role="user",
            content=request.message
        )
        db.add(user_msg)
        
        # Store assistant response
        assistant_msg = Message(
            conversation_id=conversation.id,
            user_id=user_id,  # CRITICAL FIX: Use path parameter
            role="assistant",
            content=response_text
        )
        db.add(assistant_msg)
        db.commit()
        
        print(f"✅ Chat response sent: {response_text[:100]}...")
        
        return ChatResponse(
            conversation_id=conversation.id,
            response=response_text,
            function_calls=[]
        )
        
    except Exception as e:
        import traceback
        import sys
        print(f"\n{'='*60}")
        print(f"❌ CHAT ERROR for user {user_id}")
        print(f"Message: {request.message}")
        print(f"Error: {str(e)}")
        print(f"{'='*60}")
        print("Full Traceback:")
        traceback.print_exc(file=sys.stdout)
        print(f"{'='*60}\n")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")
