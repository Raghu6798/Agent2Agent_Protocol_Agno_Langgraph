# PydanticAI Agent2Agent (A2A) Protocol Implementation

This repository demonstrates how to implement and interact with PydanticAI agents using the Agent2Agent protocol over JSON-RPC 2.0.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenRouter API key
- Required packages: `pydantic-ai`, `uvicorn`, `requests`, `python-dotenv`

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Raghu6798/Agent2Agent_Protocol_Implementation.git
cd Agent2Agent_Protocol_Implementation
```

2. **Navigate to the PydanticAI directory:**
```bash
cd pydantic_ai_agent
```

3. **Install dependencies:**
```bash
pip install pydantic-ai uvicorn requests python-dotenv
```

4. **Set up environment variables:**
Create a `.env` file in the `pydantic_ai_agent` directory:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### Running the Server

Start the PydanticAI A2A server:
```bash
uvicorn pydantic_ai_agent_poc:app --reload
```

The server will be available at: `http://127.0.0.1:8000/`

You should see output similar to:
```
INFO:     Started server process [28756]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## 📡 API Reference

### Endpoint
- **URL:** `http://127.0.0.1:8000/`
- **Method:** `POST`
- **Content-Type:** `application/json`

### Request Format

The server expects JSON-RPC 2.0 requests with the following structure:

```json
{
  "jsonrpc": "2.0",
  "id": "unique_request_id",
  "method": "tasks/send",
  "params": {
    "id": "task_id",
    "sessionId": "session_uuid",
    "acceptedOutputModes": ["text"],
    "message": {
      "role": "user",
      "parts": [
        {
          "type": "text",
          "text": "Your question or prompt here"
        }
      ]
    }
  }
}
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `jsonrpc` | string | Always "2.0" |
| `id` | string/number | Unique identifier for the request |
| `method` | string | Always "tasks/send" for A2A protocol |
| `params.id` | string | Task identifier |
| `params.sessionId` | string | Session UUID for conversation tracking |
| `params.acceptedOutputModes` | array | Output formats accepted (currently only "text") |
| `params.message.role` | string | Always "user" for input messages |
| `params.message.parts` | array | Array of message parts |
| `params.message.parts[].type` | string | Part type (currently only "text") |
| `params.message.parts[].text` | string | The actual message content |

### Response Format

The server returns responses in the following format:

```json
{
  "jsonrpc": "2.0",
  "id": "matching_request_id",
  "result": {
    "id": "task_id",
    "sessionId": "session_uuid",
    "status": {
      "state": "completed",
      "timestamp": "2025-06-05T20:41:02.893321"
    },
    "history": [
      {
        "role": "user",
        "parts": [
          {
            "type": "text",
            "text": "Your original question"
          }
        ]
      }
    ],
    "artifacts": [
      {
        "name": "result",
        "index": 0,
        "parts": [
          {
            "type": "text",
            "text": "Agent's response to your question"
          }
        ]
      }
    ]
  }
}
```

## 🧪 Testing the Server

### Using cURL

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
            "text": "Explain the difference between Mixture of Experts and Dense Feed Forward Networks"
          }
        ]
      }
    }
  }'
```




### Customizing the Agent

You can modify the agent behavior by:

1. **Changing the model:**
```python
model = OpenAIModel('gpt-4', provider=OpenRouterProvider(api_key=api_key))
```

2. **Updating the system prompt:**
```python
agent = Agent(
    model,
    system_prompt='You are a helpful AI assistant specializing in technical explanations.',
)
```

3. **Adding tools:**
```python
from pydantic_ai import Tool

async def my_tool(ctx: RunContext, query: str) -> str:
    return f"Processed: {query}"

agent = Agent(
    model,
    system_prompt='You are a helpful assistant.',
    tools=[Tool(my_tool, description="Custom tool")]
)
```

## 🛠️ Troubleshooting

### Common Issues

1. **Server not starting:**
   - Check if port 8000 is available
   - Verify all dependencies are installed
   - Ensure `.env` file contains valid `OPENROUTER_API_KEY`

2. **Connection refused:**
   - Make sure the server is running
   - Check the URL is `http://127.0.0.1:8000/` (not `localhost`)

3. **API key errors:**
   - Verify your OpenRouter API key is valid
   - Check the `.env` file is in the correct directory

4. **JSON-RPC errors:**
   - Ensure `Content-Type: application/json` header is set
   - Verify the request structure matches the expected format
   - Check that all required fields are present

### Debug Mode

Run the server with debug logging:
```bash
uvicorn pydantic_ai_agent_poc:app --reload --log-level debug
```

## 📝 Example Interactions

### Example 1: Technical Question
```json
{
  "jsonrpc": "2.0",
  "id": "req_001",
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
          "text": "How is Mixture of Experts different from Dense Feed Forward FFN?"
        }
      ]
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": "req_001",
  "result": {
    "id": "task_001",
    "sessionId": "session_001",
    "status": {
      "state": "completed",
      "timestamp": "2025-06-05T20:41:02.893321"
    },
    "artifacts": [
      {
        "name": "result",
        "index": 0,
        "parts": [
          {
            "type": "text",
            "text": "Mixture of Experts (MoE) uses sparse activation where only a subset of parameters are active per input, while Dense FFN activates all parameters, making MoE more parameter-efficient and scalable."
          }
        ]
      }
    ]
  }
}
```

## 🤝 Contributing

Feel free to submit issues and pull requests to improve this implementation.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [PydanticAI Documentation](https://ai.pydantic.dev/)
- [OpenRouter API](https://openrouter.ai/)
- [Agent2Agent Protocol Specification](https://github.com/Raghu6798/Agent2Agent_Protocol_Implementation)
