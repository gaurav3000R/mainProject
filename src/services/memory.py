"""Conversation memory management for chatbots."""

from typing import List, Dict, Any, Optional
from datetime import datetime
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from src.utils.logger import app_logger


class ConversationMemoryManager:
    """
    Manage conversation history with in-memory storage.
    Can be extended to use persistent storage (Redis, PostgreSQL, etc.)
    """
    
    def __init__(self, max_messages_per_conversation: int = 20):
        """
        Initialize memory manager.
        
        Args:
            max_messages_per_conversation: Maximum messages to keep per conversation
        """
        self._conversations: Dict[str, ChatMessageHistory] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}
        self.max_messages = max_messages_per_conversation
        app_logger.info(f"Initialized ConversationMemoryManager (max_messages={max_messages_per_conversation})")
    
    def get_history(self, conversation_id: str) -> BaseChatMessageHistory:
        """
        Get or create conversation history.
        
        Args:
            conversation_id: Unique conversation identifier
            
        Returns:
            Chat message history for this conversation
        """
        if conversation_id not in self._conversations:
            self._conversations[conversation_id] = ChatMessageHistory()
            self._metadata[conversation_id] = {
                "created_at": datetime.now().isoformat(),
                "message_count": 0,
                "last_activity": datetime.now().isoformat()
            }
            app_logger.info(f"Created new conversation: {conversation_id}")
        
        # Update last activity
        self._metadata[conversation_id]["last_activity"] = datetime.now().isoformat()
        
        return self._conversations[conversation_id]
    
    def add_message(self, conversation_id: str, message: BaseMessage):
        """
        Add a message to conversation history.
        
        Args:
            conversation_id: Conversation identifier
            message: Message to add
        """
        history = self.get_history(conversation_id)
        history.add_message(message)
        
        # Update metadata
        self._metadata[conversation_id]["message_count"] += 1
        
        # Trim if exceeds max
        self._trim_history(conversation_id)
        
        app_logger.debug(f"Added message to {conversation_id} (total: {len(history.messages)})")
    
    def add_user_message(self, conversation_id: str, content: str):
        """Add a user message."""
        self.add_message(conversation_id, HumanMessage(content=content))
    
    def add_ai_message(self, conversation_id: str, content: str):
        """Add an AI message."""
        self.add_message(conversation_id, AIMessage(content=content))
    
    def get_messages(self, conversation_id: str) -> List[BaseMessage]:
        """
        Get all messages for a conversation.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            List of messages
        """
        history = self.get_history(conversation_id)
        return history.messages
    
    def get_recent_messages(self, conversation_id: str, n: int = 10) -> List[BaseMessage]:
        """
        Get recent N messages.
        
        Args:
            conversation_id: Conversation identifier
            n: Number of recent messages to retrieve
            
        Returns:
            List of recent messages
        """
        messages = self.get_messages(conversation_id)
        return messages[-n:] if messages else []
    
    def clear_conversation(self, conversation_id: str):
        """
        Clear a specific conversation.
        
        Args:
            conversation_id: Conversation identifier
        """
        if conversation_id in self._conversations:
            self._conversations[conversation_id].clear()
            self._metadata[conversation_id]["message_count"] = 0
            app_logger.info(f"Cleared conversation: {conversation_id}")
    
    def delete_conversation(self, conversation_id: str):
        """
        Delete a conversation entirely.
        
        Args:
            conversation_id: Conversation identifier
        """
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
            del self._metadata[conversation_id]
            app_logger.info(f"Deleted conversation: {conversation_id}")
    
    def get_conversation_metadata(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get metadata for a conversation.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            Conversation metadata
        """
        return self._metadata.get(conversation_id, {})
    
    def list_conversations(self) -> List[Dict[str, Any]]:
        """
        List all conversations with metadata.
        
        Returns:
            List of conversation info
        """
        return [
            {
                "conversation_id": conv_id,
                **self._metadata[conv_id]
            }
            for conv_id in self._conversations.keys()
        ]
    
    def get_conversation_summary(self, conversation_id: str) -> str:
        """
        Get a text summary of the conversation.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            Summary string
        """
        messages = self.get_messages(conversation_id)
        if not messages:
            return "No messages in conversation"
        
        summary_parts = []
        for msg in messages:
            role = "User" if isinstance(msg, HumanMessage) else "AI"
            content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
            summary_parts.append(f"{role}: {content}")
        
        return "\n".join(summary_parts)
    
    def _trim_history(self, conversation_id: str):
        """
        Trim conversation history to max_messages.
        Keeps the most recent messages.
        """
        history = self._conversations[conversation_id]
        if len(history.messages) > self.max_messages:
            # Keep most recent messages
            trimmed = history.messages[-self.max_messages:]
            history.clear()
            for msg in trimmed:
                history.add_message(msg)
            app_logger.debug(f"Trimmed conversation {conversation_id} to {self.max_messages} messages")


# Global singleton instance
memory_manager = ConversationMemoryManager()
