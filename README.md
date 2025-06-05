# Agent2Agent Protocol (A2A)

![[A2A Protocol](https://placeholder.com/banner.png) ](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/image5_VkAG0Kd.original.png)<!-- Add actual banner image if available -->

An open protocol enabling communication and interoperability between opaque agentic applications.

## 🌟 What's the Hype About?

The Agent2Agent (A2A) protocol addresses a critical challenge in the AI landscape: enabling gen AI agents, built on diverse frameworks by different companies running on separate servers, to communicate and collaborate effectively - as **agents**, not just as tools. A2A provides a common language for agents, fostering a more interconnected, powerful, and innovative AI ecosystem.

## 🚀 Why A2A?

As AI agents become more prevalent, their ability to interoperate is crucial for building complex, multi-functional applications:

| Key Benefit | Description |
|-------------|-------------|
| **Break Down Silos** | Connect agents across different ecosystems |
| **Enable Complex Collaboration** | Allow specialized agents to work together on tasks beyond single-agent capabilities |
| **Promote Open Standards** | Foster community-driven agent communication |
| **Preserve Opacity** | Collaborate without exposing internal state or proprietary logic |

## Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) package manager

## Available Agents

The repository contains the following agentic framework 
implementations:

1. Agno Agents
2. Langraph Agents
3. LlamaIndex Agents
4. Pydantic AI Agents (documentation available in its directory)

## Running the Agents

Each agent implementation is located in its own directory. To run any agent:

1. First, clone the repository:
```
git clone https://github.com/Raghu6798/Agent2Agent_Protocol_Implementation.git

cd Agent2Agent_Protocol_Implementation/<agent_directory>:
```

2. Start the agent server:
   ```bash
   uv run .
   ```

The agent server will start on `localhost:10000`.

## Testing the Agents

Each agent implementation comes with a test client that can send JSON-RPC 2.0 requests to the running agent server. To test an agent:

1. Make sure the agent server is running (see above)
2. In a new terminal, navigate to the agent's directory
3. Run the test client:
   ```bash
   uv run test_client.py  # or test_agno_client.py for Agno agents
   ```

### Agent-Specific Details

#### Agno Agents
```bash
cd agno_agents
uv run .  # Start server
uv run test_agno_client.py  # Run client
```

#### Langraph Agents
```bash
cd langraph
uv run .  # Start server
uv run test_client.py  # Run client
```

#### LlamaIndex Agents
```bash
cd llama_index_agents
uv run .  # Start server
uv run test_client.py  # Run client
```

## Protocol Details

All agents implement the JSON-RPC 2.0 protocol and listen on `localhost:10000`. The test clients demonstrate how to:

- Connect to the agent server
- Send JSON-RPC 2.0 requests
- Handle responses from the agent
- Process any errors that may occur

## Notes

- Each agent implementation may have specific requirements or configurations. Check the respective agent's directory for additional documentation.
- Make sure to run the agent server before attempting to use the test client.
- The test clients are provided as examples of how to interact with the agents using JSON-RPC 2.0.
- For Pydantic AI Agents, please refer to the documentation in its directory.
