#  Langraph Addition Agent

A simple arithmetic agent built with Langraph that specializes in addition operations. This agent is part of the Agent2Agent Protocol implementation using JSON-RPC 2.0.

## 🎯 What Does the Addition Agent Do?

The agent is a focused arithmetic assistant that:
- Performs addition operations using a dedicated calculator tool
- Uses Google's Gemini 2.0 Flash model for natural language understanding
- Provides clear, step-by-step calculation explanations
- Handles basic addition requests with proper error handling

> ℹ️ This agent is built using Langraph and Google's Gemini model, specifically designed for addition operations.

## 🚀 Getting Started

### ✅ Prerequisites
- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager
- Google API Key (set in `.env` as `GOOGLE_API_KEY`)

### 🛠️ Running the Agent Server

1. First, clone the repository and Navigate to the langgraph agents repo :
```
git clone https://github.com/Raghu6798/Agent2Agent_Protocol_Implementation.git

cd Agent2Agent_Protocol_Implementation/langraph:
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

#### `.invoke(query: str, session_id: str) -> str`
Processes an addition request and returns the result.

Example:
```python
result = agent.invoke("What's 5 plus 3?", "session_123")
# Returns: "Let me calculate that for you...\n5 + 3 = 8\nThe sum is 8"
```

#### `.stream(query: str, sessionId: str) -> AsyncIterator[dict]`
Streams the calculation process in real-time, showing:
- When the calculation starts
- Tool usage status
- Final result

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
    "method": "calculate",
    "params": {
      "query": "What is 7 plus 4?",
      "sessionId": "session_001"
    }
  }'
```

### 📥 Supported Content Types
- `text`
- `text/plain`

## 🧠 How It Works

1. **Input Processing**
   - Receives natural language addition requests
   - Uses Gemini model to understand the request
   - Extracts numbers to be added

2. **Calculation**
   - Uses the `add_two_numbers` tool for actual calculation
   - Provides step-by-step explanation
   - Returns formatted result

3. **Response Format**
   - Starts with "Let me calculate that for you..."
   - Shows the calculation process
   - Ends with the final sum

## 📁 Project Structure

| File | Purpose |
|------|---------|
| `langgraph_agent.py` | Core addition agent implementation |
| `__main__.py` | Server entry point |
| `test_client.py` | Test client for local testing |
| `.env` | API keys and environment variables |

## 🔐 Environment Setup

Create a `.env` file in the project root with:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

## 📝 Example Usage

### Basic Addition
```python
# Input
"What's 5 plus 3?"

# Output
"Let me calculate that for you...
5 + 3 = 8
The sum is 8"
```

### Error Handling
```python
# Input
"What's 5 times 3?"

# Output
"I'm sorry, I can only handle addition operations. Please use a different tool for multiplication."
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
