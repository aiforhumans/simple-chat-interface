from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MessageHistory:
    messages: List[Dict[str, str]]
    timestamp: datetime
    conversation_id: str

class MessageFormatter:
    def __init__(self):
        self.history: List[MessageHistory] = []

    def format_message(self, role: str, content: str) -> Dict[str, str]:
        """Format a single message into the expected structure."""
        return {"role": role, "content": content}

    def create_system_message(self, content: str) -> Dict[str, str]:
        """Create a system message."""
        return self.format_message("system", content)

    def create_user_message(self, content: str) -> Dict[str, str]:
        """Create a user message."""
        return self.format_message("user", content)

    def create_assistant_message(self, content: str) -> Dict[str, str]:
        """Create an assistant message."""
        return self.format_message("assistant", content)

    def create_conversation(self, messages: List[Dict[str, str]], conversation_id: str = None) -> MessageHistory:
        """Create and store a new conversation history."""
        history = MessageHistory(
            messages=messages,
            timestamp=datetime.now(),
            conversation_id=conversation_id or str(len(self.history))
        )
        self.history.append(history)
        return history

    def get_conversation(self, conversation_id: str) -> MessageHistory:
        """Retrieve a conversation by its ID."""
        for history in self.history:
            if history.conversation_id == conversation_id:
                return history
        return None

    def add_to_conversation(self, conversation_id: str, role: str, content: str) -> MessageHistory:
        """Add a new message to an existing conversation."""
        history = self.get_conversation(conversation_id)
        if history:
            history.messages.append(self.format_message(role, content))
        return history