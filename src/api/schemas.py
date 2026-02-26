"""
Request/Response DTOs (Data Transfer Objects)
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class MessageRequest(BaseModel):
    """User message request"""
    conversation_id: str = Field(..., description="Conversation ID")
    content: str = Field(..., description="Message content", min_length=1, max_length=5000)
    user_id: str = Field(default="default_user", description="User ID")

class MessageResponse(BaseModel):
    """Agent message response"""
    response: str = Field(..., description="Agent response text")
    tool_used: Optional[str] = Field(None, description="Tool that was used")
    tool_input: Optional[Dict[str, Any]] = Field(None, description="Input parameters for tool")
    tool_output: Optional[Dict[str, Any]] = Field(None, description="Output from tool")
    reasoning: str = Field(..., description="Reasoning behind the response")

class ConversationCreateRequest(BaseModel):
    """Create conversation request"""
    user_id: str = Field(default="default_user", description="User ID")
    title: str = Field(default="New Conversation", description="Conversation title")

class ConversationResponse(BaseModel):
    """Conversation response"""
    id: str = Field(..., description="Conversation ID")
    user_id: str = Field(..., description="User ID")
    title: str = Field(..., description="Conversation title")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    is_active: bool = Field(..., description="Is conversation active")

class ConversationHistoryResponse(BaseModel):
    """Conversation history response"""
    conversation_id: str = Field(..., description="Conversation ID")
    messages: List[Dict[str, Any]] = Field(..., description="List of messages")
    total_messages: int = Field(..., description="Total message count")

class ToolInfo(BaseModel):
    """Tool information"""
    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")

class ToolsListResponse(BaseModel):
    """Available tools response"""
    tools: List[ToolInfo] = Field(..., description="List of available tools")
    total_tools: int = Field(..., description="Total tools count")

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(..., description="Response timestamp")

class ErrorResponse(BaseModel):
    """Error response"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error detail")
    timestamp: datetime = Field(..., description="Error timestamp")

