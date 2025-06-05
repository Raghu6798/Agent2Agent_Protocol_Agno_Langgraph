# 🧠 Langraph Agent – Agent2Agent Protocol Implementation

This agent is part of the Langraph Agents implementation under the Agent2Agent Protocol using JSON-RPC 2.0. The Langraph Agent leverages the powerful Langraph framework for advanced agent orchestration, workflow management, and complex multi-agent interactions.

## 🎯 What Does the Langraph Agent Do?

The Langraph Agent is a sophisticated autonomous agent system designed to:
- Orchestrate complex multi-agent workflows using Langraph's graph-based architecture
- Manage state and context across agent interactions
- Execute parallel and sequential agent tasks
- Handle complex reasoning chains and decision trees
- Provide robust error handling and recovery mechanisms

> ℹ️ This agent is built on the Langraph framework, enabling powerful graph-based agent orchestration and workflow management.

## 🚀 Getting Started

### ✅ Prerequisites
- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager
- Dependencies from root `pyproject.toml`
- OpenAI API Key (set in `.env` as `OPENAI_API_KEY`)

### 🛠️ Running the Agent Server

1. Navigate to the agent directory:
   ```bash
   cd a2a_poc/langraph
   ```

2. Start the server:
   ```bash
   uv run .
   ```

📡 The server will run on `http://localhost:10000`

### 🧪 Testing the Agent

Run the test client in a new terminal to simulate a JSON-RPC request:
```bash
uv run test_client.py
```

## 🔧 Implementation Details

### Code Location
The agent is defined in:
```bash
langraph/langgraph_agent.py
```

### Key Methods

#### `.invoke(query: str, session_id: str = None) -> dict`
Processes a request through the Langraph workflow and returns structured results.

Returns a response object containing:
- `status`: Current execution status
- `result`: The processed result
- `workflow_state`: Current state of the workflow
- `metadata`: Additional execution metadata

#### `.stream(query: str, session_id: str = None) -> AsyncIterator[dict]`
Streams workflow execution updates in real-time.
- Emits state transitions
- Workflow progress updates
- Intermediate results
- Error states and recovery attempts

## 📤 API Usage

### JSON-RPC 2.0 Interface

The agent can be accessed via the JSON-RPC 2.0 interface.

#### Sample Request
```bash
curl -X POST http://127.0.0.1:8000/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test_001",
    "method": "workflow/execute",
    "params": {
      "id": "workflow_001",
      "sessionId": "session_001",
      "workflow": {
        "type": "sequential",
        "steps": [
          {
            "agent": "reasoning",
            "input": "Analyze the following problem: ..."
          },
          {
            "agent": "execution",
            "input": "Based on the analysis, execute the following steps: ..."
          }
        ]
      }
    }
  }'
```

### 📥 Supported Content Types
The Langraph Agent supports the following MIME types:
- `application/json`
- `text/plain`

## 🧠 Implementation Notes

- Built on Langraph's graph-based architecture for flexible workflow management
- Supports both sequential and parallel agent execution
- Implements robust state management and context preservation
- Provides comprehensive error handling and recovery mechanisms
- Enables dynamic workflow modification during execution

## 📁 Project Structure

| File | Purpose |
|------|---------|
| `langgraph_agent.py` | Core agent implementation using Langraph |
| `lang_agent_executor.py` | Langraph workflow execution logic |
| `__main__.py` | Server entry point |
| `test_client.py` | Test client for local testing |
| `.env` | API keys and environment variables |

## 🔐 Environment Setup

Create a `.env` file in the project root with:
```env
OPENAI_API_KEY=your_api_key_here
LANGCHAIN_API_KEY=your_langchain_key_here  # Optional
```

## 📊 Workflow Types

The agent supports several workflow patterns:

1. **Sequential Workflows**
   - Linear execution of agent steps
   - State preservation between steps
   - Conditional branching

2. **Parallel Workflows**
   - Concurrent agent execution
   - Result aggregation
   - Resource optimization

3. **Graph-based Workflows**
   - Complex agent interaction patterns
   - Dynamic routing
   - State management across nodes

## 📝 Additional Resources

- [Langraph Documentation](https://python.langchain.com/docs/langgraph)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)

## 🔍 Example Workflows

### Basic Sequential Workflow
```python
workflow = {
    "type": "sequential",
    "steps": [
        {
            "agent": "analyzer",
            "input": "Initial analysis task"
        },
        {
            "agent": "executor",
            "input": "Execute based on analysis"
        }
    ]
}
```

### Parallel Workflow
```python
workflow = {
    "type": "parallel",
    "branches": [
        {
            "agent": "researcher",
            "input": "Research task 1"
        },
        {
            "agent": "researcher",
            "input": "Research task 2"
        }
    ],
    "aggregator": "merge_results"
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. When contributing:
1. Follow the existing code style
2. Add tests for new features
3. Update documentation as needed
4. Ensure all workflows are properly typed

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔄 State Management

The agent implements sophisticated state management:
- Persistent session states
- Workflow state tracking
- Context preservation
- Error state recovery
- State serialization and deserialization

## 🛡️ Error Handling

Comprehensive error handling includes:
- Workflow validation
- Agent execution errors
- State recovery
- Timeout management
- Resource cleanup
