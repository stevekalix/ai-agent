"""
Database models for the AI Agent System
"""

from sqlalchemy import Column, String, DateTime, Integer, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Conversation(Base):
    """Conversation session model"""
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(50), index=True)
    title = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id}, title={self.title})>"

class Message(Base):
    """Message model for conversation history"""
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, index=True)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), index=True)
    role = Column(String(20), index=True)  # "user" or "agent"
    content = Column(Text)
    tool_used = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role}, tool_used={self.tool_used})>"

class AgentLog(Base):
    """Agent execution logs"""
    __tablename__ = "agent_logs"

    id = Column(String(36), primary_key=True, index=True)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), index=True)
    action = Column(String(100))
    tool_name = Column(String(100))
    input_data = Column(Text)
    output_data = Column(Text)
    execution_time = Column(Integer)  # milliseconds
    status = Column(String(20))  # "success", "failure"
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<AgentLog(id={self.id}, tool={self.tool_name}, status={self.status})>"

