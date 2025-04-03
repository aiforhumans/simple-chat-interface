import pytest
from datetime import datetime
from message_formatter import MessageFormatter, MessageHistory
from chat import ChatClient, ChatResponse
from unittest.mock import Mock, patch

# MessageFormatter tests
def test_message_formatter_creation():
    formatter = MessageFormatter()
    assert formatter.history == []

def test_message_formatting():
    formatter = MessageFormatter()
    message = formatter.format_message("user", "Hello")
    assert message == {"role": "user", "content": "Hello"}

def test_conversation_creation():
    formatter = MessageFormatter()
    messages = [
        formatter.create_system_message("Be helpful"),
        formatter.create_user_message("Hi")
    ]
    
    conversation = formatter.create_conversation(messages)
    assert isinstance(conversation, MessageHistory)
    assert len(conversation.messages) == 2
    assert conversation.conversation_id == "0"

def test_conversation_retrieval():
    formatter = MessageFormatter()
    messages = [formatter.create_user_message("Hello")]
    conversation = formatter.create_conversation(messages, "test-id")
    
    retrieved = formatter.get_conversation("test-id")
    assert retrieved == conversation

def test_add_to_conversation():
    formatter = MessageFormatter()
    messages = [formatter.create_user_message("Hello")]
    conversation = formatter.create_conversation(messages, "test-id")
    
    formatter.add_to_conversation("test-id", "assistant", "Hi there!")
    assert len(conversation.messages) == 2
    assert conversation.messages[-1]["content"] == "Hi there!"

# ChatClient tests
@pytest.fixture
def mock_openai():
    with patch('openai.OpenAI') as mock:
        yield mock

@pytest.fixture
def chat_client(mock_openai):
    return ChatClient()

def test_chat_completion(chat_client, mock_openai):
    # Create mock response
    mock_completion = Mock()
    mock_completion.choices = [Mock(message=Mock(content="Test response"))]
    mock_completion.usage = Mock(total_tokens=10)
    
    # Set up the mock chain correctly
    mock_chat = Mock()
    mock_completions = Mock()
    mock_completions.create = Mock(return_value=mock_completion)
    mock_chat.completions = mock_completions
    chat_client.client.chat = mock_chat
    
    messages = [{"role": "user", "content": "Hello"}]
    response = chat_client.complete(messages)
    
    assert isinstance(response, ChatResponse)
    assert response.content == "Test response"
    assert response.tokens == 10

def test_chat_error_handling(chat_client, mock_openai):
    # Set up the mock chain correctly
    mock_chat = Mock()
    mock_completions = Mock()
    mock_completions.create = Mock(side_effect=Exception("API Error"))
    mock_chat.completions = mock_completions
    chat_client.client.chat = mock_chat
    
    messages = [{"role": "user", "content": "Hello"}]
    response = chat_client.complete(messages)
    
    assert response.content == ""
    assert response.tokens == 0

def test_response_formatting(chat_client):
    response = ChatResponse(content="Hello", tokens=10, generation_time=1.5)
    formatted = chat_client.format_response(response)
    
    assert "Hello" in formatted
    assert "10" in formatted
    assert "1.50s" in formatted

# Integration test
def test_basic_conversation_flow():
    formatter = MessageFormatter()
    messages = [
        formatter.create_system_message("Be helpful"),
        formatter.create_user_message("Hi")
    ]
    
    # Create and verify conversation
    conversation = formatter.create_conversation(messages)
    assert len(conversation.messages) == 2
    
    # Add response and verify
    formatter.add_to_conversation(conversation.conversation_id, "assistant", "Hello!")
    assert len(conversation.messages) == 3
    assert conversation.messages[-1]["content"] == "Hello!"

if __name__ == "__main__":
    pytest.main([__file__])
