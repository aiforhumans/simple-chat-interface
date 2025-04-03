import os
import time
from typing import Dict, List, Tuple, Optional
from openai import OpenAI
from dataclasses import dataclass
from message_formatter import MessageFormatter

@dataclass
class ChatResponse:
    content: str
    tokens: int
    generation_time: float

class ChatClient:
    def __init__(
        self,
        api_key: str = os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
        base_url: str = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
        timeout: float = 30.0,
        default_model: str = "model-identifier"
    ):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout
        )
        self.default_model = default_model
        self.formatter = MessageFormatter()

    def complete(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        model: Optional[str] = None,
        stream: bool = False
    ) -> ChatResponse:
        try:
            start_time = time.time()
            completion = self.client.chat.completions.create(
                model=model or self.default_model,
                messages=messages,
                temperature=temperature,
                stream=stream
            )
            generation_time = time.time() - start_time
            
            return ChatResponse(
                content=completion.choices[0].message.content,
                tokens=completion.usage.total_tokens,
                generation_time=generation_time
            )
            
        except Exception as e:
            print(f"Error occurred: {e}")
            return ChatResponse(content="", tokens=0, generation_time=0.0)

    @staticmethod
    def format_response(response: ChatResponse) -> str:
        separator = "-" * 50
        return f"""
{separator}
Response:
{response.content}

Metrics:
- Total tokens: {response.tokens}
- Generation time: {response.generation_time:.2f}s
{separator}
"""

def main():
    chat_client = ChatClient()
    formatter = chat_client.formatter
    
    # Create a new conversation
    messages = [
        formatter.create_system_message("Always answer in rhymes."),
        formatter.create_user_message("Introduce yourself.")
    ]
    
    # Store the conversation
    conversation = formatter.create_conversation(messages)
    
    # Get the response
    response = chat_client.complete(messages)
    
    # Add the assistant's response to the conversation
    formatter.add_to_conversation(
        conversation.conversation_id,
        "assistant",
        response.content
    )
    
    # Print the formatted output
    formatted_output = chat_client.format_response(response)
    print(formatted_output)

if __name__ == "__main__":
    main()
