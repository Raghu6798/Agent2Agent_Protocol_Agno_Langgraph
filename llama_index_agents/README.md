# 🎨 LlamaIndex Brand Image Agent

A sophisticated AI-powered brand image generation agent built with LlamaIndex that creates professional marketing visuals using natural language descriptions. This agent is part of the Agent2Agent Protocol implementation using JSON-RPC 2.0.

## 🎯 What Does the Brand Image Agent Do?

The agent is a specialized marketing assistant that:
- Generates professional product images using AI
- Creates optimized marketing prompts
- Handles complete brand image generation workflows
- Uses Together AI's FLUX.1.1[Schnell] model for image generation
- Leverages Llama 3.3 8B for natural language understanding

## 🚀 Getting Started

### ✅ Prerequisites
- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager
- Together AI API Key (set in `.env` as `TOGETHER_API_KEY`)
- OpenRouter API Key (set in `.env` as `OPENROUTER_API_KEY`)

### 🛠️ Running the Agent Server

1. First, clone the repository and Navigate to the llama_index agent directory::
```
git clone https://github.com/Raghu6798/Agent2Agent_Protocol_Implementation.git

cd Agent2Agent_Protocol_Implementation/lama_index_agents:
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
llama_index_agents/llama_index_agent.py
```

### Key Methods

#### `.invoke(query: str, session_id: str = None) -> str`
Processes a brand image generation request and returns the result.

Example:
```python
result = agent.invoke(
    "Generate a brand image for a luxury watch called 'Chronos Elite' with a minimalist design and gold accents",
    "session_123"
)
```

#### `.stream(query: str, session_id: str = None) -> AsyncIterator[dict]`
Streams the image generation process in real-time, showing:
- Initial analysis
- Marketing prompt creation
- Image generation progress
- Final result with image URL

## 📤 API Usage

### JSON-RPC 2.0 Interface

The agent can be accessed via the JSON-RPC 2.0 interface.

#### cURL Example
```bash
curl -X POST http://localhost:10000/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test_001",
    "method": "generate_brand_image",
    "params": {
      "query": "Create a brand image for a premium coffee brand called 'Morning Brew' with earthy tones and rustic style",
      "sessionId": "session_001"
    }
  }'
```

#### Postman Collection
```json
{
  "info": {
    "name": "Brand Image Agent API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Generate Brand Image",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "url": "http://localhost:10000",
        "body": {
          "mode": "raw",
          "raw": {
            "jsonrpc": "2.0",
            "id": "test_001",
            "method": "generate_brand_image",
            "params": {
              "query": "Create a brand image for a premium coffee brand called 'Morning Brew' with earthy tones and rustic style",
              "sessionId": "session_001"
            }
          }
        }
      }
    }
  ]
}
```

### 📥 Supported Content Types
- `text`
- `text/plain`

## 🎨 Image Generation Features

### Marketing Prompt Creation
The agent can create optimized prompts for:
- Product photography
- Brand visuals
- Marketing materials
- Social media content

### Image Generation Parameters
- Model: FLUX.1-schnell-Free
- Style: Professional marketing photography
- Quality: High-end commercial grade
- Customization: Brand colors, visual style, product placement

## 📁 Project Structure

| File | Purpose |
|------|---------|
| `llama_index_agent.py` | Core brand image agent implementation |
| `llama_index_agent_executor.py` | Agent execution logic |
| `__main__.py` | Server entry point |
| `test_client.py` | Test client for local testing |
| `.env` | API keys and environment variables |

## 🔐 Environment Setup

Create a `.env` file in the project root with:
```env
TOGETHER_API_KEY=your_together_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## 📝 Example Usage

### Basic Brand Image Generation
```python
# Input
"Generate a brand image for a luxury skincare product called 'Glow Essence' with minimalist packaging and pastel colors"

# Output
"Starting brand image generation...
Analyzing product requirements...
Creating marketing prompt...
Generating brand image...
Image generated successfully! URL: https://..."
```

### Complete Workflow
```python
# Input with specific parameters
{
    "product_name": "EcoTech Water Bottle",
    "description": "Sustainable stainless steel water bottle with bamboo lid",
    "brand_colors": "Forest green and natural wood tones",
    "visual_style": "Eco-friendly and modern minimalist"
}

# Output
"Brand generation completed for EcoTech Water Bottle. 
Marketing prompt created and image generated successfully. 
Direct URL: https://..."
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Important Notes

- The agent requires valid API keys for both Together AI and OpenRouter
- Image generation may take a few seconds depending on the complexity
- All generated images are temporary and should be downloaded if needed
- The agent is optimized for product and brand marketing visuals
- Streaming responses provide real-time progress updates
