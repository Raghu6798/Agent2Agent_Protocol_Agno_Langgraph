# Agno Agents Implementation

This directory contains the Agno Agents implementation of the Agent2Agent Protocol using JSON-RPC 2.0.

## Overview

The Agno Agents implementation provides a robust agent system using the Agno framework, featuring:
- JSON-RPC 2.0 server implementation
- Custom agent executor
- Comprehensive test client

## Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Dependencies specified in `pyproject.toml`

## Running the Agent Server

1. Make sure you're in the agno_agents directory:
   ```bash
   cd a2a_poc/agno_agents
   ```

2. Start the agent server:
   ```bash
   uv run .
   ```

The server will start on `localhost:10000`.

## Testing the Agent

1. Ensure the agent server is running (see above)
2. In a new terminal, navigate to the agno_agents directory
3. Run the test client:
   ```bash
   uv run test_agno_client.py
   ```

## Implementation Details

- `agno_agent.py`: Core agent implementation
- `agno_agent_executor.py`: Custom executor for the agent
- `__main__.py`: Server entry point
- `test_agno_client.py`: Test client with example requests

## Available Methods

The agent server implements the following JSON-RPC 2.0 methods:
- `process_request`: Main method for processing agent requests
- Additional methods as documented in the test client

## Notes

- The agent server must be running before using the test client
- Check the test client implementation for example requests and responses
- The agent uses the Agno framework for enhanced agent capabilities
