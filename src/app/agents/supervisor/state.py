from typing_extensions import TypedDict


class AgentState(TypedDict):
    # User and context
    customer_id: str
    query: str

    # Intent classification
    intent: str
    confidence: float

    # Agent processing
    agent_response: str
    escalation_requested: bool
    conversation_history: list[dict[str, str]]
