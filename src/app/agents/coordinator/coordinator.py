from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from pydantic import BaseModel, Field

from typing_extensions import TypedDict, Literal

load_dotenv()

model = "gpt-4o-mini"
agent = ChatOpenAI(model=model, temperature=0.0, max_tokens=500)

class AgentState(TypedDict):
    # User and context
    customer_id: str
    query: str
    
    # Intent classification
    intent: Literal["account", "transaction", "unknown"]
    confidence: float
    
    # Agent processing
    agent_response: str
    escalation_requested: bool
    conversation_history: list[dict[str, str]]  # List of messages with role and content
    

def load_memory_node(state: AgentState) -> AgentState:
    """
    Load customer context and conversation history.
    In a real system, this would query a database or memory store.
    """
    # TODO: Replace with actual memory retrieval
    # For now, just initialize empty if not present
    if not state.get("conversation_history"):
        state["conversation_history"] = []

    print(f"[Memory] Loaded context for customer {state['customer_id']}")
    return state

class IntentClassifier(BaseModel):
    user_intent: Literal["account", "transaction", "unknown"] = Field(
        ...,
        description='Classify whether the user wants to request information about their credit limit (account), check their latest transactions (transaction), or if the intent is unknown (unknown).'
    )
    
def coordinator(state: AgentState) -> AgentState:
    if not state.get("query") or not isinstance(state["query"], str) or not state["query"].strip():
        state["intent"] = "unknown"
        state["confidence"] = 0.0
        print("[Intent classifier] No valid query provided")
        return state

    prompt = """
    You are an intent classification model.
    Classify whether the user wants to request information about their credit limit (account),
    check their latest transactions (transaction),
    or if the intent is unknown (unknown) and you require clarification."""

    intent_cls_llm = agent.with_structured_output(IntentClassifier)

    try:
        intent_result = intent_cls_llm.invoke([
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": state["query"]
            }
        ])

        intent = intent_result.user_intent if isinstance(intent_result, IntentClassifier) else intent_result.get("user_intent", "unknown")
        state["intent"] = intent
        state["confidence"] = 0.95

        print(f"[Intent classifier] Classified intent: {state['intent']} with confidence {state['confidence']}")
    except Exception as e:
        state["intent"] = "unknown"
        state["confidence"] = 0.0
        print(f"[Intent classifier] Error classifying intent: {e}")

    return state


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

    print("Testing coordinator with query:", state_tmp["query"])
    result = coordinator(state_tmp)
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
        result = coordinator(test_state)
        print(f"  → Intent: {result['intent']}, Confidence: {result['confidence']}")
