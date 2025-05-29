
import os
from googlesearch import search
from uuid import uuid4
from typing import Annotated

from collections.abc import AsyncIterable
from typing import List, Dict, Optional, Any
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_cerebras import ChatCerebras
from pydantic import BaseModel

from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from firecrawl import FirecrawlApp

load_dotenv()

CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
os.environ["CEREBRAS_API_KEY"] = os.getenv("CEREBRAS_API_KEY")

memory = InMemorySaver()
session_id = str(uuid4())

class ResponseSchema(BaseModel):
    response: str






@tool
def add_two_numbers(
    a: Annotated[int, "The first number to add"],
    b: Annotated[int, "The second number to add"]
) -> Annotated[int, "The sum of the two numbers"]:
    """
    Adds two integers together and returns the result.
    
    Examples:
        >>> add_two_numbers(2, 3)
        5
        >>> add_two_numbers(-1, 1)
        0
    """
    return a + b

SYSTEM_PROMPTS = """You are a precise arithmetic assistant that specializes in basic math operations. 

## Instructions:
1. You have access to a calculator tool that can add two numbers
2. When given a math problem:
   - First determine if it requires addition
   - Extract the exact numbers from the request
   - Always use the add_two_numbers tool for calculations
   - Present the result clearly
3. For non-addition requests:
   - Politely explain you only handle addition
   - Suggest using a different tool for other operations

## Response Format:
- Start with "Let me calculate that for you..."
- Show the equation: "{a} + {b} = {result}"
- End with "The sum is {result}"

## Examples:
User: What's 5 plus 3?
Assistant: Let me calculate that for you...
5 + 3 = 8
The sum is 8

User: Add 10 and -2
Assistant: Let me calculate that for you...
10 + (-2) = 8
The sum is 8
"""

class AdditionAgent:
    def __init__(self):
        self.model = ChatCerebras(
            model="llama-4-scout-17b-16e-instruct",
            temperature=0.4,
            max_tokens=512,
        )
        self.tools = [add_two_numbers]
        self.graph = create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt=SYSTEM_PROMPTS,
            checkpointer=memory,
        )

    def invoke(self, query, session_id) -> str:
        config = {'configurable': {'thread_id': session_id}}
        
        # Create proper message format
        messages = [{"role": "user", "content": query}]
        
        try:
            result = self.graph.invoke(
                {"messages": messages},
                config
            )
            
            # Extract the final response
            if result and 'messages' in result:
                for message in reversed(result['messages']):
                    if hasattr(message, 'content') and message.content:
                        return message.content
                    elif isinstance(message, dict) and 'content' in message:
                        return message['content']
            
            return "Unable to process the request."
        
        except Exception as e:
            return f"Error occurred: {str(e)}"

    async def stream(self, query, sessionId) -> AsyncIterable[Dict[str, Any]]:
        inputs = {'messages': [{'role': 'user', 'content': query}]}
        config = {'configurable': {'thread_id': sessionId}}

        async for item in self.graph.astream(inputs, config, stream_mode='values'):
            if 'messages' in item and item['messages']:
                message = item['messages'][-1]
                
                if (
                    isinstance(message, AIMessage)
                    and hasattr(message, 'tool_calls')
                    and message.tool_calls
                ):
                    yield {
                        'is_task_complete': False,
                        'require_user_input': False,
                        'content': 'Searching for information...',
                    }
                elif isinstance(message, ToolMessage):
                    yield {
                        'is_task_complete': False,
                        'require_user_input': False,
                        'content': 'Processing the search results...',
                    }
                elif isinstance(message, AIMessage) and not hasattr(message, 'tool_calls'):
                    # Final response
                    yield {
                        'is_task_complete': True,
                        'require_user_input': False,
                        'content': message.content,
                    }

    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']