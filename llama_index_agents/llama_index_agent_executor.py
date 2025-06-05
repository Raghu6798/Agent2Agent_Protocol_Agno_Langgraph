import logging
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import Event, EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    InternalError,
    InvalidParamsError,
    Part,
    Task,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import (
    new_agent_text_message,
    new_task,
)
from a2a.utils.errors import ServerError
from llama_index_agent import BrandImageAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrandGenAgentExecutor(AgentExecutor):
    """Addition Agent Executor with proper event queue handling."""
    
    def __init__(self):
        self.agent = BrandImageAgent()
    
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        # Validate request first
        error = self._validate_request(context)
        if error:
            raise ServerError(error=InvalidParamsError())
        
        # Check if event queue is still open
        if not hasattr(event_queue, 'is_closed') or event_queue.is_closed():
            logger.error("Event queue is already closed")
            raise ServerError(error=InternalError())
        
        query = context.get_user_input()
        task = context.current_task
        
        if not task:
            task = new_task(context.message)
            # Only enqueue if queue is still open
            if not event_queue.is_closed():
                event_queue.enqueue_event(task)
            else:
                logger.error("Cannot enqueue task - queue is closed")
                raise ServerError(error=InternalError())
        
        updater = TaskUpdater(event_queue, task.id, task.contextId)
        
        try:
            async for item in self.agent.stream(query, task.contextId):
                # Check if queue is still open before each update
                if event_queue.is_closed():
                    logger.warning("Event queue closed during streaming - stopping execution")
                    break
                
                is_task_complete = item['is_task_complete']
                require_user_input = item['require_user_input']
                
                if not is_task_complete and not require_user_input:
                    # Add status message for tool execution
                    logger.info(f"Tool execution status: {item['content']}")
                    updater.update_status(
                        TaskState.working,
                        new_agent_text_message(
                            item['content'],
                            task.contextId,
                            task.id,
                        ),
                    )
                elif require_user_input:
                    updater.update_status(
                        TaskState.input_required,
                        new_agent_text_message(
                            item['content'],
                            task.contextId,
                            task.id,
                        ),
                        final=True,
                    )
                    break
                else:
                    # Final result
                    updater.add_artifact(
                        [Part(root=TextPart(text=item['content']))],
                        name='addition_result',  # Changed from 'conversion_result'
                    )
                    updater.complete()
                    break
        
        except Exception as e:
            logger.error(f'An error occurred while streaming the response: {e}')
            # Try to update status even if there's an error, but check queue first
            if not event_queue.is_closed():
                try:
                    updater.update_status(
                        TaskState.error,
                        new_agent_text_message(
                            "An error occurred during calculation",
                            task.contextId,
                            task.id,
                        ),
                        final=True,
                    )
                except:
                    pass  # Queue might have closed during error handling
            raise ServerError(error=InternalError()) from e
    
    def _validate_request(self, context: RequestContext) -> bool:
        # Add actual validation logic if needed
        user_input = context.get_user_input()
        if not user_input or not user_input.strip():
            logger.error("Empty user input")
            return True
        return False
    
    async def cancel(
        self, request: RequestContext, event_queue: EventQueue
    ) -> Task | None:
        # Implement proper cancellation if needed
        logger.info("Cancellation requested")
        raise ServerError(error=UnsupportedOperationError())