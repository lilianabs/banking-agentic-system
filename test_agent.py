from src.app.agents.supervisor.state import AgentState
from src.app.agents.supervisor.graph import supervisor

if __name__ == "__main__":
    # Test the intent classification with a sample state
    state_tmp = AgentState({
        "customer_id": "12345",
        "query": "I'd like to know the business hours of one of your branches.",
        "conversation_history": [],
        "intent": "unknown",
        "confidence": 0.0,
        "agent_response": "",
        "escalation_requested": False,
    })

    print("Testing supervisor with query:", state_tmp["query"])
    result = supervisor(state_tmp)
    print(f"Result - Intent: {result['intent']}, Confidence: {result['confidence']}")

    # Test with different queries
    test_queries = [
        "What is my account balance?",
        "Show me my recent transactions",
        "I need help with something",
        ""  # Empty query test
    ]

    for query in test_queries:
        test_state = AgentState({
            "customer_id": "12345",
            "query": query,
            "conversation_history": [],
            "intent": "unknown",
            "confidence": 0.0,
            "agent_response": "",
            "escalation_requested": False,
        })

        print(f"\nTesting query: '{query}'")
        result = supervisor(test_state)
        print(f"  → Intent: {result['intent']}, Confidence: {result['confidence']}")