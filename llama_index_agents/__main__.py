import logging
import os

import click
import httpx

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore, InMemoryPushNotifier
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from llama_index_agent import BrandImageAgent
from llama_index_agent_executor import BrandGenAgentExecutor
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""
    pass


@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=10000)
def main(host, port):
    """Starts the Llama Index Brand Image Generation server."""
    try:
        if not os.getenv('OPENROUTER_API_KEY'):
            raise MissingAPIKeyError(
                'OPENROUTER API KEY environment variable not set.'
            )

        capabilities = AgentCapabilities(streaming=True, pushNotifications=True)

        skill = AgentSkill(
            id="Brand_Image_Generation_Agent",
            name="Deep_Research_agent",
            description="Generates an Image of a brand given it's metadata",
            tags=['Image Gen']
        )

        agent_card = AgentCard(
            name='Integer Addition Agent',
            description='Just an Addition Agent',
            url='http://localhost:10000/',
            version='1.0.0',
            defaultInputModes=['text/plain'],
            defaultOutputModes=['text/plain'],
            capabilities=AgentCapabilities(streaming=True),
            skills=[skill],
        )

        httpx_client = httpx.AsyncClient()
        request_handler = DefaultRequestHandler(
            agent_executor=BrandGenAgentExecutor(),
            task_store=InMemoryTaskStore(),
            push_notifier=InMemoryPushNotifier(httpx_client),
        )
        server = A2AStarletteApplication(
            agent_card=agent_card,
            http_handler=request_handler
        )

        import uvicorn
        uvicorn.run(server.build(), host=host, port=port)

    except MissingAPIKeyError as e:
        logger.error(f'Error: {e}')
        exit(1)
    except Exception as e:
        logger.error(f'An error occurred during server startup: {e}')
        exit(1)


if __name__ == '__main__':
    main()
