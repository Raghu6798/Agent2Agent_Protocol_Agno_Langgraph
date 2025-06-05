import os
from uuid import uuid4
from typing import Annotated, AsyncIterable, Dict, Any
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from loguru import logger
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

memory = InMemorySaver()

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
    logger.info(f"Adding {a} + {b}")
    result = a + b
    logger.info(f"Result: {result}")
    return result

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
- Show the calculation process
- End with a clear result

## Examples:
User: What's 5 plus 3?
Assistant: Let me calculate that for you...
[Using calculator tool]
5 + 3 = 8
The sum is 8
"""

class AdditionAgent:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
        self.tools = [add_two_numbers]
        self.graph = create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt=SYSTEM_PROMPTS,
            checkpointer=memory,
        )

    def invoke(self, query, session_id) -> str:
        config = {'configurable': {'thread_id': session_id}}
        
        messages = [HumanMessage(content=query)]
        
        try:
            result = self.graph.invoke(
                {"messages": messages},
                config
            )
            
            if result and 'messages' in result:
                for message in reversed(result['messages']):
                    if hasattr(message, 'content') and message.content:
                        return message.content
                    elif isinstance(message, dict) and 'content' in message:
                        return message['content']
            
            return "Unable to process the request."
        
        except Exception as e:
            logger.error(f"Error in invoke: {e}")
            return f"Error occurred: {str(e)}"

    async def stream(self, query: str, sessionId: str) -> AsyncIterable[Dict[str, Any]]:
        """Stream the agent's response with proper event handling."""
        inputs = {'messages': [HumanMessage(content=query)]}
        config = {'configurable': {'thread_id': sessionId}}
        
        logger.info(f"Starting stream for query: {query}")
        
        try:
            has_yielded_final = False
            tool_call_in_progress = False
            
            async for chunk in self.graph.astream(inputs, config, stream_mode='values'):
                logger.debug(f"Stream chunk: {chunk}")
                
                if 'messages' in chunk and chunk['messages']:
                    message = chunk['messages'][-1]
                    
                    # Handle AI message with tool calls
                    if (isinstance(message, AIMessage) and 
                        hasattr(message, 'tool_calls') and 
                        message.tool_calls):
                        
                        if not tool_call_in_progress:
                            tool_call_in_progress = True
                            logger.info("Tool call detected - yielding status")
                            yield {
                                'is_task_complete': False,
                                'require_user_input': False,
                                'content': 'Calculating the sum...',
                            }
                    
                    # Handle tool response
                    elif isinstance(message, ToolMessage):
                        logger.info("Tool response received")
                        yield {
                            'is_task_complete': False,
                            'require_user_input': False,
                            'content': 'Processing calculation result...',
                        }
                    
                    # Handle final AI response (without tool calls)
                    elif (isinstance(message, AIMessage) and 
                          not hasattr(message, 'tool_calls') and 
                          message.content and 
                          not has_yielded_final):
                        
                        logger.info("Final response ready")
                        has_yielded_final = True
                        yield {
                            'is_task_complete': True,
                            'require_user_input': False,
                            'content': message.content,
                        }
                        break 
            
            # Ensure we always yield a final response
            if not has_yielded_final:
                logger.warning("No final response yielded - providing fallback")
                yield {
                    'is_task_complete': True,
                    'require_user_input': False,
                    'content': 'Calculation completed, but no result was generated.',
                }
        
        except Exception as e:
            logger.error(f"Error in stream: {e}", exc_info=True)
            yield {
                'is_task_complete': True,
                'require_user_input': False,
                'content': f'An error occurred during calculation: {str(e)}',
            }

    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']