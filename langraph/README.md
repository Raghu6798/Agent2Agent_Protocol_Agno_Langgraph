### GeoPal: LangGraph Geospatial Agent

A sophisticated geospatial agent built with LangGraph that leverages OpenRouteService capabilities through a custom MCP server. This agent is part of the Agent2Agent Protocol implementation using JSON-RPC 2.0.

## 🎯 What Does GeoPal Do?

GeoPal is a specialized geospatial assistant that:

- Processes natural language queries about locations, routes, and points of interest
- Leverages OpenRouteService tools through a custom MCP server
- Provides intelligent routing, navigation, and location-based recommendations
- Generates interactive visualizations for spatial data
- Solves complex vehicle routing problems and optimizes travel itineraries


> ℹ️ This agent is built using LangGraph, OpenRouteService, and the Agent2Agent protocol, designed specifically for geospatial intelligence tasks.



## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.8+
- [OpenRouteService API key](https://openrouteservice.org/dev/#/signup)
- OpenRouter API key (for LLM access)
- Required Python packages (see requirements.txt)


### 🛠️ Running the Agent Server

1. First, clone the repository:


```shellscript
git clone https://github.com/yourusername/geopal-agent.git
cd geopal-agent
```

2. Install dependencies:


```shellscript
pip install -r requirements.txt
```

3. Set up environment variables:


```shellscript
# Create .env file with your API keys
echo "OPENROUTER_API_KEY=your_openrouter_key_here" > .env
echo "OPENROUTE_SERVICE_API=your_ors_key_here" >> .env
```

4. Start the MCP server:


```shellscript
python mcp_server.py
```

5. In a new terminal, start the A2A server:


```shellscript
python -m a2a.server.apps --host localhost --port 10000
```

📡 The A2A server will run on `http://localhost:10000`

### 🧪 Testing the Agent

Run the test client in a new terminal to interact with the agent:

```shellscript
python a2a_client.py --agent http://localhost:10000
```

## 🔧 Implementation Details

### Core Components

#### 1. LangGraph Agent (`ORSAgent`)

The agent orchestrates the workflow and handles natural language understanding:

```python
# Located in langgraph_agent.py
class ORSAgent:
    """ORSAgent - a specialized assistant for OpenRouteService routing queries."""
    
    # Core methods
    async def invoke(self, query: str, context_id: str) -> dict[str, Any]
    async def stream(self, query: str, context_id: str) -> AsyncIterable[dict[str, Any]]
```

#### 2. MCP Server Tools

The MCP server provides specialized geospatial tools:

| Tool | Description
|-----|-----
| `get_directions` | Calculates routes between locations
| `geocode_address` | Converts addresses to coordinates
| `get_isochrones` | Creates reachability maps
| `get_pois` | Finds points of interest
| `get_poi_names` | Gets simplified POI name lists
| `optimize_vehicle_routes` | Solves complex routing problems
| `create_simple_delivery_problem` | Creates delivery optimization problems
| `optimize_traveling_salesman` | Solves TSP problems


#### 3. A2A Server

Handles communication with clients using the Agent2Agent protocol.

## 📤 API Capabilities

### 🗺️ Geospatial Intelligence

#### Geocoding

```python
# Convert address to coordinates
result = await geocode_address("Brandenburg Gate, Berlin, Germany")
```

#### Point of Interest Discovery

```python
# Find POIs near coordinates with 500m radius
pois = await get_pois((13.377704, 52.516431), buffer=500, limit=10)
```

### 🚗 Advanced Routing

#### Route Planning

```python
# Calculate route between Berlin and Munich
route = await get_directions(
    [(13.377704, 52.516431), (11.581981, 48.135125)], 
    profile="driving-car"
)
```

#### Isochrone Analysis

```python
# Create 15-minute reachability map
isochrone = await get_isochrones(
    [(13.377704, 52.516431)],
    profile="walking",
    range=[900]  # 15 minutes in seconds
)
```

### 📦 Logistics Optimization

#### Vehicle Routing

```python
# Optimize delivery routes for multiple vehicles
solution = await optimize_vehicle_routes(jobs, vehicles)
```

#### Traveling Salesman Problem

```python
# Find optimal route visiting multiple locations
optimal_route = await optimize_traveling_salesman(locations)
```

## 🧠 How It Works

1. **Query Processing**

1. Receives natural language geospatial queries
2. Uses Mistral model to understand the request
3. Determines required geospatial tools



2. **Tool Execution**

1. Calls appropriate OpenRouteService tools via MCP
2. Processes and transforms geospatial data
3. Generates visualizations when appropriate



3. **Response Generation**

1. Formats results in user-friendly language
2. Provides detailed routing instructions
3. Includes links to interactive maps when available





## 📁 Project Structure

| File | Purpose
|-----|-----
| `langgraph_agent.py` | Core agent implementation
| `mcp_server.py` | OpenRouteService MCP server
| `a2a_server.py` | Agent2Agent protocol server
| `a2a_client.py` | Test client for interaction
| `.env` | API keys and environment variables


## 🔐 Environment Variables

Create a `.env` file with:

```plaintext
OPENROUTER_API_KEY=your_openrouter_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTE_SERVICE_API=your_ors_key_here
```

## 📝 Example Queries

### Route Planning

```plaintext
"What's the fastest route from Berlin to Munich by car?"
```

### POI Discovery

```plaintext
"Find me hotels and restaurants within 500 meters of the Brandenburg Gate"
```

### Isochrone Analysis

```plaintext
"Show me areas I can reach within 15 minutes walking from my current location"
```

### Delivery Optimization

```plaintext
"I need to deliver packages to these 5 addresses. What's the most efficient route?"
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Related Projects

- [LangGraph](https://github.com/langchain-ai/langgraph) - Framework for building stateful, multi-actor applications with LLMs
- [OpenRouteService](https://openrouteservice.org/) - Services for geospatial analysis
- [Agent2Agent Protocol](https://github.com/a2a-protocol/a2a-protocol) - Protocol for agent communication


## 🌟 Features

### Current Capabilities

- ✅ Natural language understanding of geospatial queries
- ✅ Advanced routing with multiple transportation modes
- ✅ POI discovery with 600+ categories
- ✅ Interactive map generation
- ✅ Vehicle routing optimization
- ✅ Streaming responses for real-time updates


### Roadmap

- 🔜 Multi-agent collaboration for complex travel planning
- 🔜 Integration with real-time traffic data
- 🔜 Support for public transportation routing
- 🔜 User preference learning for personalized recommendations
