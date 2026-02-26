"""
Agent routes - Main API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database.init_db import get_db
from src.database.repository import ConversationRepository, MessageRepository, AgentLogRepository
from src.api.schemas import (
    MessageRequest, MessageResponse, ConversationCreateRequest, ConversationResponse,
    ConversationHistoryResponse, ToolsListResponse, ToolInfo, ErrorResponse
)
from src.agent.core import conversation_manager
from src.agent.tools import tool_registry
from src.logging_config import logger
import uuid
import json
import time

router = APIRouter()

# ==================== Conversation Management ====================

@router.post("/conversation", response_model=ConversationResponse)
async def create_conversation(
    request: ConversationCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new conversation"""
    try:
        conversation = ConversationRepository.create(
            db=db,
            user_id=request.user_id,
            title=request.title
        )
        logger.info(f"Created conversation {conversation.id}")
        return ConversationResponse(
            id=conversation.id,
            user_id=conversation.user_id,
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            is_active=conversation.is_active
        )
    except Exception as e:
        logger.error(f"Error creating conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversation/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Get conversation details"""
    try:
        conversation = ConversationRepository.get_by_id(db, conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        return ConversationResponse(
            id=conversation.id,
            user_id=conversation.user_id,
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            is_active=conversation.is_active
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{user_id}")
async def get_user_conversations(
    user_id: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get all conversations for a user"""
    try:
        conversations = ConversationRepository.get_user_conversations(db, user_id, limit)
        return {
            "user_id": user_id,
            "total": len(conversations),
            "conversations": [
                {
                    "id": c.id,
                    "title": c.title,
                    "created_at": c.created_at,
                    "updated_at": c.updated_at
                }
                for c in conversations
            ]
        }
    except Exception as e:
        logger.error(f"Error retrieving conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== Message Processing ====================

@router.post("/message", response_model=MessageResponse)
async def process_message(
    request: MessageRequest,
    db: Session = Depends(get_db)
):
    """Process user message and get agent response"""
    try:
        # Validate conversation exists
        conversation = ConversationRepository.get_by_id(db, request.conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Record start time
        start_time = time.time()

        # Process message with agent
        agent_response = conversation_manager.process_message(request.content)

        # Save user message
        MessageRepository.create(
            db=db,
            conversation_id=request.conversation_id,
            role="user",
            content=request.content
        )

        # Save agent response
        MessageRepository.create(
            db=db,
            conversation_id=request.conversation_id,
            role="assistant",
            content=agent_response["response"],
            tool_used=agent_response["tool_used"]
        )

        # Log agent execution
        if agent_response["tool_used"]:
            AgentLogRepository.create(
                db=db,
                conversation_id=request.conversation_id,
                action="tool_execution",
                tool_name=agent_response["tool_used"],
                input_data=json.dumps(agent_response["tool_input"]),
                output_data=json.dumps(agent_response["tool_output"]),
                execution_time=int((time.time() - start_time) * 1000),
                status="success" if agent_response["tool_output"].get("success") else "failure"
            )

        logger.info(f"Message processed in conversation {request.conversation_id}")

        return MessageResponse(
            response=agent_response["response"],
            tool_used=agent_response["tool_used"],
            tool_input=agent_response["tool_input"],
            tool_output=agent_response["tool_output"],
            reasoning=agent_response["reasoning"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversation/{conversation_id}/history", response_model=ConversationHistoryResponse)
async def get_conversation_history(
    conversation_id: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get conversation message history"""
    try:
        # Validate conversation exists
        conversation = ConversationRepository.get_by_id(db, conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        messages = MessageRepository.get_conversation_history(db, conversation_id, limit)

        return ConversationHistoryResponse(
            conversation_id=conversation_id,
            messages=[
                {
                    "id": m.id,
                    "role": m.role,
                    "content": m.content,
                    "tool_used": m.tool_used,
                    "created_at": m.created_at
                }
                for m in messages
            ],
            total_messages=len(messages)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== Tools Information ====================

@router.get("/tools", response_model=ToolsListResponse)
async def list_tools():
    """List all available tools"""
    try:
        tools_info = tool_registry.get_all_tools_info()
        tools = [
            ToolInfo(name=name, description=desc)
            for name, desc in tools_info.items()
        ]
        logger.info(f"Retrieved {len(tools)} tools")
        return ToolsListResponse(tools=tools, total_tools=len(tools))
    except Exception as e:
        logger.error(f"Error retrieving tools: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tools/{tool_name}/execute")
async def execute_tool_directly(
    tool_name: str,
    params: dict,
    db: Session = Depends(get_db)
):
    """Execute a tool directly (for testing)"""
    try:
        logger.info(f"Direct tool execution: {tool_name}")
        result = tool_registry.execute_tool(tool_name, **params)
        return result
    except Exception as e:
        logger.error(f"Error executing tool: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== Statistics ====================

@router.get("/conversation/{conversation_id}/stats")
async def get_conversation_stats(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Get conversation statistics"""
    try:
        conversation = ConversationRepository.get_by_id(db, conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        messages = MessageRepository.get_conversation_history(db, conversation_id, 1000)
        logs = AgentLogRepository.get_conversation_logs(db, conversation_id, 1000)

        user_messages = [m for m in messages if m.role == "user"]
        assistant_messages = [m for m in messages if m.role == "assistant"]
        successful_tools = [l for l in logs if l.status == "success"]

        return {
            "conversation_id": conversation_id,
            "total_messages": len(messages),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "total_tool_executions": len(logs),
            "successful_tool_executions": len(successful_tools),
            "failed_tool_executions": len(logs) - len(successful_tools),
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

