import os 
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext,Tool
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openrouter import OpenRouterProvider
import warnings

warnings.filterwarnings('ignore')

load_dotenv()

model = OpenAIModel(
    'anthropic/claude-3.5-haiku',
    provider=OpenRouterProvider(api_key=os.getenv('OPENROUTER_API_KEY')),
)

agent = Agent(
    model,
    system_prompt='Be concise, reply with one sentence.',  
)
app = agent.to_a2a()

