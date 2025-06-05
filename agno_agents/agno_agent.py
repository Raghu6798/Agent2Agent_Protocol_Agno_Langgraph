import os
from textwrap import dedent
from dotenv import load_dotenv
from loguru import logger
from typing import AsyncIterator, Iterator
from agno.run.response import RunResponse
from agno.agent import Agent
from agno.models.cerebras import Cerebras
from agno.tools.youtube import YouTubeTools
from agno.storage.sqlite import SqliteStorage
import time
import json

load_dotenv()

class YouTubeAgent:
    def __init__(self):
        self.agent_storage: str = "tmp/agents.db"

        self.agent = Agent(
            name="YouTube Agent",
            model=Cerebras(id="llama-4-scout-17b-16e-instruct", api_key=os.getenv("CEREBRAS_API_KEY")),
            tools=[YouTubeTools()],
            show_tool_calls=True,
            instructions=dedent("""\
                You are an expert YouTube content analyst with a keen eye for detail! 🎓
                 
                IMPORTANT: You MUST follow these steps in order for EVERY video analysis:
                1. ALWAYS start by using get_youtube_video_data to fetch basic video information
                2. ALWAYS use get_youtube_captions to fetch the video transcript
                3. ONLY proceed with analysis after BOTH tool calls are successful
                4. NEVER skip any of these steps or proceed without the data
                
                Required Steps for EVERY Analysis:
                1. Video Data Collection (MANDATORY)
                   - Call get_youtube_video_data with the video URL
                   - Verify you received the video metadata
                   - Call get_youtube_captions with the same URL
                   - Verify you received the captions
                   - Only proceed after BOTH calls succeed
                
                2. Video Overview
                   - Start with a clear title and author
                   - Note video length and type
                   - Identify main topics/themes
                   - Create a brief introduction
                
                3. Content Analysis
                   - Break down the video into key sections
                   - Create timestamps for important moments
                   - Summarize each major section
                   - Highlight key points and insights
                
                4. Final Summary
                   - Provide a comprehensive overview
                   - List main takeaways
                   - Include all relevant timestamps
                   - End with a conclusion
                
                Format Guidelines:
                - Use markdown for better readability
                - Start with ## Video Analysis
                - Use ### for major sections
                - Use bullet points for key points
                - Format timestamps as [MM:SS]
                
                Quality Requirements:
                - NEVER proceed without both tool calls
                - Verify data before analysis
                - Ensure comprehensive coverage
                - Maintain consistent detail level
                - Focus on valuable insights
                
                Error Handling:
                - If a tool call fails, explain the error
                - Request user to verify the URL
                - Do not proceed with partial data
                - Always be clear about what's missing
            """),
            storage=SqliteStorage(
                table_name="Youtube_Agent",
                db_file=self.agent_storage
            ),
            add_datetime_to_instructions=True,
            add_history_to_messages=True,
            num_history_responses=5,
            markdown=True,
        )

    def invoke(self, query: str, session_id: str = None) -> list[dict]:
        try:
            logger.info(f"Invoking YouTube Agent with query: {query}")
            result = self.agent.run(query)
            
            # Handle RunResponse object
            if isinstance(result, RunResponse):
                response_content = []
                
                # Handle tool calls
                if result.tools:
                    logger.info(f"Tool call detected: {result.tools}")
                    response_content.append({
                        "is_task_complete": False,
                        "require_user_input": False,
                        "content": f"Using tool: {result.tools}"
                    })
                
                # Handle main content
                if result.content is not None:
                    response_content.append({
                        "is_task_complete": True,
                        "require_user_input": False,
                        "content": str(result.content)
                    })
                
                # Log any extra data
                if result.extra_data:
                    if hasattr(result.extra_data, 'reasoning_steps'):
                        logger.debug(f"Reasoning steps: {result.extra_data.reasoning_steps}")
                    if hasattr(result.extra_data, 'reasoning_messages'):
                        logger.debug(f"Reasoning messages: {result.extra_data.reasoning_messages}")
                
                return response_content or [{
                    "is_task_complete": True,
                    "require_user_input": False,
                    "content": "No response generated."
                }]
            
            # Handle other response types
            return [{
                "is_task_complete": True,
                "require_user_input": False,
                "content": str(result)
            }]
            
        except Exception as e:
            logger.error(f"Error during invoke: {e}", exc_info=True)
            return [{
                "is_task_complete": True,
                "require_user_input": False,
                "content": f"Error: {str(e)}"
            }]

    def stream(self, query: str, session_id: str = None) -> Iterator[dict]:
        try:
            response_stream = self.agent.run(query, session_id=session_id, stream=True)

            for chunk in response_stream:
                if isinstance(chunk, RunResponse):
                    if chunk.content:
                        yield {
                            "is_task_complete": False,
                            "require_user_input": False,
                            "content": str(chunk.content)
                        }
                    
                    # Handle tool calls more directly
                    if chunk.tools:
                        yield {
                            "is_task_complete": False,
                            "require_user_input": False,
                            "content": f"Executing tool: {chunk.tools}"
                        }
            
            # Final completion
            yield {
                "is_task_complete": True,
                "require_user_input": False,
                "content": "Analysis completed."
            }
        
        except Exception as e:
            yield {
                "is_task_complete": True,
                "require_user_input": False,
                "content": f"Error: {str(e)}"
            }

    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']
