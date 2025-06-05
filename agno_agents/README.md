# 🧠 YouTube Agent – Agno Agent Implementation

This agent is part of the Agno Agents implementation under the Agent2Agent Protocol using JSON-RPC 2.0. The YouTube Agent performs intelligent video analysis by leveraging tool-based data retrieval and the Cerebras language model.

## 🎯 What Does the YouTube Agent Do?

The YouTube Agent is a multimodal autonomous agent designed to:
- Retrieve YouTube video metadata and captions using Agno tools
- Analyze video structure, themes, and timestamps
- Generate detailed, human-readable markdown summaries of YouTube content
- Follow strict step-by-step logic for consistent analysis quality

> ℹ️ This agent is built with Cerebras as the LLM backend and uses YouTubeTools for interacting with video data.

## 🚀 Getting Started

### ✅ Prerequisites
- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager
- API Key for Cerebras (set in `.env` as `CEREBRAS_API_KEY`)
- Dependencies from `pyproject.toml`

### 🛠️ Running the Agent Server

1. Navigate to the agent directory:
   ```bash
   cd a2a_poc/agno_agents
   ```

2. Start the server:
   ```bash
   uv run .
   ```

📡 The server will run on `http://localhost:10000`

### 🧪 Testing the Agent

Run the test client in a new terminal to simulate a JSON-RPC request:
```bash
uv run test_agno_client.py
```

## 🔧 Implementation Details

### Code Location
The agent is defined in:
```bash
agno_agents/youtube_agent.py
```

### Key Methods

#### `.invoke(query: str, session_id: str = None) -> list[dict]`
Synchronously processes a YouTube URL and returns structured markdown analysis.

Returns a list of response segments, each containing:
- `is_task_complete`: Whether the task is done
- `require_user_input`: If further input is needed
- `content`: The actual markdown analysis or message

#### `.stream(query: str, session_id: str = None) -> Iterator[dict]`
Streams response chunks while the video is being analyzed.
- Emits tool usage
- Content updates
- Final completion status

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
    "method": "tasks/send",
    "params": {
      "id": "task_001",
      "sessionId": "session_001",
      "acceptedOutputModes": ["text"],
      "message": {
        "role": "user",
        "parts": [
          {
            "type": "text",
            "text": "I need you to help me summarize this video : [https://www.youtube.com/watch?v=dQw4w9WgXcQ](https://youtu.be/oWZbcq_figk?si=NWTivR8jm9xQJSrJ)"
          }
        ]
      }
    }
  }'
```

### 📥 Supported Content Types
The YouTube Agent supports the following MIME types:
- `text`
- `text/plain`

## 🧠 Implementation Notes

- The agent never proceeds without fetching both video metadata and captions
- All results are markdown-formatted for clarity
- Built on top of the Agno framework, enabling flexible agent behavior and tool usage
- Responses are structured as lists of JSON objects for integration with frontend or downstream pipelines

## 📁 Project Structure

| File | Purpose |
|------|---------|
| `youtube_agent.py` | YouTube-specific agent logic |
| `agno_agent_executor.py` | Custom execution logic for agents |
| `__main__.py` | Server entry point |
| `test_agno_client.py` | Simulated client for local testing |
| `.env` | API keys and environment variables |

## 🔐 Environment Setup

Create a `.env` file in the project root with:
```env
CEREBRAS_API_KEY=your_api_key_here
```

## 📝 Additional Resources

- [Agno Framework Documentation](https://github.com/agno-ai/agno)
- [Cerebras API Documentation](https://docs.cerebras.net)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
