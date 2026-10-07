# Agentic banking system

This repo contains the code of a multi-agent banking system.

## Multi-agent system

This multi-agentic system consist of the following agent and subagents:

1. **Coordinator Agent**
   - Detects intent and routes to corresponding agent.
   - If the intent is not clear, asks further questions to the customer to better understand the query.

2. **Accounts Agent** (original + RAG)
   - Tool: `get_account_balance(account_id)`
   - RAG: answer policy/product questions from a knowledge base
     - "What are the requirements for a credit limit increase?"
     - "Can I get a credit limit increase?"

3. **Transactions Agent**
   - Tool: `get_transaction_history(account_id)`
   - Tool: 
