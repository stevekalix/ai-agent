"""
Database repository for data access operations
"""

from sqlalchemy.orm import Session
from src.database.models import Conversation, Message, AgentLog
from src.logging_config import logger
from datetime import datetime
import uuid

class ConversationRepository:
    """Repository for conversation operations"""

    @staticmethod
    def create(db: Session, user_id: str, title: str) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=title
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        logger.info(f"Created conversation {conversation.id} for user {user_id}")
        return conversation

    @staticmethod
    def get_by_id(db: Session, conversation_id: str) -> Conversation:
        """Get conversation by ID"""
        return db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()

    @staticmethod
    def get_user_conversations(db: Session, user_id: str, limit: int = 10):
        """Get user's conversations"""
        return db.query(Conversation).filter(
            Conversation.user_id == user_id,
            Conversation.is_active == True
        ).order_by(Conversation.updated_at.desc()).limit(limit).all()

    @staticmethod
    def update_timestamp(db: Session, conversation_id: str):
        """Update conversation timestamp"""
        conversation = ConversationRepository.get_by_id(db, conversation_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(conversation)

class MessageRepository:
    """Repository for message operations"""

    @staticmethod
    def create(db: Session, conversation_id: str, role: str, content: str, tool_used: str = None) -> Message:
        """Create a new message"""
        message = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_used=tool_used
        )
        db.add(message)
        db.commit()
        db.refresh(message)

        # Update conversation timestamp
        ConversationRepository.update_timestamp(db, conversation_id)
        logger.debug(f"Created message {message.id} in conversation {conversation_id}")
        return message

    @staticmethod
    def get_conversation_history(db: Session, conversation_id: str, limit: int = 50):
        """Get conversation history"""
        return db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).limit(limit).all()

class AgentLogRepository:
    """Repository for agent log operations"""

    @staticmethod
    def create(
        db: Session,
        conversation_id: str,
        action: str,
        tool_name: str,
        input_data: str,
        output_data: str,
        execution_time: int,
        status: str,
        error_message: str = None
    ) -> AgentLog:
        """Create a new agent log"""
        log = AgentLog(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            action=action,
            tool_name=tool_name,
            input_data=input_data,
            output_data=output_data,
            execution_time=execution_time,
            status=status,
            error_message=error_message
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        logger.debug(f"Created agent log {log.id} for tool {tool_name}")
        return log

    @staticmethod
    def get_conversation_logs(db: Session, conversation_id: str, limit: int = 100):
        """Get logs for a conversation"""
        return db.query(AgentLog).filter(
            AgentLog.conversation_id == conversation_id
        ).order_by(AgentLog.created_at.desc()).limit(limit).all()

