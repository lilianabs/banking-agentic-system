# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Banking Agentic System** is a multi-agent banking assistant built with LangChain and LangGraph. It demonstrates both single-agent and multi-agent patterns for handling banking customer queries through a coordinator agent that routes requests to specialized subagents.

## Development Setup

- **Python version**: 3.13+
- **Dependency manager**: `uv` (see `pyproject.toml`)
- **Environment**: Uses `.env` file for API keys (OpenAI)
- **Development platform**: Jupyter notebooks (in `notebooks/`)

### Install dependencies
```bash
uv sync
```

### Run the main notebook
```bash
jupyter notebook notebooks/agents.ipynb
```

### Activate the virtual environment (if needed)
```bash
source .venv/bin/activate
```

## Architecture

The system implements a hierarchical multi-agent architecture:

1. **Coordinator Agent** (`coordinator_agent`)
   - Entry point for all user queries
   - Routes requests to appropriate subagents based on query type
   - Synthesizes responses from multiple subagents

2. **Specialized Subagents** (each with scoped tools):
   - **Accounts Subagent**: Account balance queries (`get_account_balance`)
   - **Transactions Subagent**: Transaction history (`get_transaction_history`)
   - **Services Subagent**: Address/customer service queries (`get_current_address`)

3. **Banking Tools** (mock implementations for demonstration)
   - `get_account_balance(account_id)`: Returns mock account balance
   - `get_transaction_history(account_id)`: Returns mock transaction list
   - `get_current_address(account_id)`: Returns mock address

### Tool Invocation Pattern
Each tool is wrapped with `@tool` decorator and integrated via `create_agent()`. Subagents call each other through tool wrappers (e.g., `call_accounts_subagent`), allowing the coordinator to orchestrate multi-step queries.

## Key Dependencies

- **langchain**: Agent framework and chat model integration
- **langchain-openai**: OpenAI model support (gpt-4o-mini)
- **langgraph**: Not actively used yet but available for graph-based agent execution
- **jupyter/notebook**: Development environment
- **python-dotenv**: Load `.env` for API credentials

## Configuration

The system uses environment variables (loaded via `dotenv`):
- `OPENAI_API_KEY`: Required for LLM calls

Set these in `.env` (not tracked in git).

## Testing

Currently, functionality is tested manually in the notebook (`notebooks/agents.ipynb`). Two examples are provided:
- Simple single-agent query for account balance
- Multi-agent query combining account balance and address retrieval

## Notes for Future Development

- **Real data**: Mock tool implementations return hardcoded data. Replace with actual database/API calls.
- **LangGraph integration**: `langgraph` is installed but unused; consider using it for more complex agent coordination patterns (e.g., conditional routing, loops).
- **Error handling**: Current code lacks error handling for API failures or invalid account IDs.
- **Production deployment**: Notebook-based development is suitable for prototyping; move to `.py` modules for production.
