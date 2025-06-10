import asyncio
import os
from dotenv import load_dotenv
from typing import List, TypedDict, Annotated

from loguru import logger
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.types import CachePolicy
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.prebuilt import ToolNode

from langchain_mcp_adapters.client import MultiServerMCPClient

# Load environment variables
load_dotenv()

# Setup logging configuration (optional: change format or level here)
logger.add(
    "ors_agent.log",
    rotation="10 MB",  # or time-based like "00:00" daily rotation
    retention="10 days",
    enqueue=True,     # Enable thread/process safe logging
    backtrace=True,
    diagnose=True,
)  # Save logs to file

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
logger.info(f"MISTRAL_API_KEY loaded: {'Yes' if MISTRAL_API_KEY else 'No'}")
if MISTRAL_API_KEY:
    logger.info(f"MISTRAL_API_KEY starts with: {MISTRAL_API_KEY[:10]}...")
else:
    logger.error("MISTRAL_API_KEY environment variable not set.")
    raise ValueError("MISTRAL_API_KEY environment variable not set. Please set it in your .env file.")

ORS_SERVER_PATH = os.path.join(os.path.dirname(__file__), "ors_mcp_server.py")

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

async def run_ors_agent():
    logger.info("Initializing ORS FastMCP server connection...")
    mcp_client = MultiServerMCPClient(
        {
           "geo_pal": {
            "url": "https://server.smithery.ai/@Raghu6798/geopal_traveling_and_logistics/mcp?api_key=e3b06a92-b690-4c3a-9e46-fa480791e61b&profile=cognitive-weasel-8FCgUK",
            "transport": "streamable_http",
        }
        }
    )

    logger.info("Loading ORS tools from FastMCP server...")
    tools = await mcp_client.get_tools(server_name="geo_pal")
    logger.debug(f"Loaded {len(tools)} tools: {[t.name for t in tools]}")

    logger.info("Initializing Mistral AI model...")
    model = ChatMistralAI(
        model="mistral-small-latest",
        api_key=MISTRAL_API_KEY
    )
    logger.info("Mistral AI model initialized successfully")
    model_with_tools = model.bind_tools(tools)

    def call_model(state: AgentState):
        messages = state["messages"]
        logger.debug(f"Calling model with messages: {messages}")
        response = model_with_tools.invoke(messages)
        return {"messages": response}

    tool_node = ToolNode(tools)

    builder = StateGraph(AgentState)
    builder.add_node("llm", call_model)
    builder.add_node("tools", tool_node)
    builder.add_edge(START, "llm")

    builder.add_conditional_edges(
        "llm",
        lambda state: "tools" if state["messages"][-1].tool_calls else END,
    )

    builder.add_edge("tools", "llm")

    async with AsyncSqliteSaver.from_conn_string(":memory:") as memory:
        agent_executor = builder.compile(checkpointer=memory)

        while True:
            query = input("\nEnter your query (type 'bye' or 'exit' to quit): ").strip()
            if query.lower() in {"bye", "exit"}:
                print("Exiting the agent. Goodbye!")
                break

            thread_id = f"user_thread_{hash(query) % 10000}"  # simple thread id

            logger.info(f"Running query for thread: {thread_id} -> {query}")
            try:
                result = await agent_executor.ainvoke(
                    {"messages": [HumanMessage(content=query)]},
                    config={"configurable": {"thread_id": thread_id}}
                )
                final_response = result["messages"][-1].content
                logger.success(f"Final response for {thread_id}: {final_response}")
                print(f"\n--- {thread_id} ---\n{final_response}")
            except Exception as e:
                logger.exception(f"Error while processing {thread_id}: {e}")

if __name__ == "__main__":
    logger.info("Starting ORS agent runner")
    asyncio.run(run_ors_agent())
