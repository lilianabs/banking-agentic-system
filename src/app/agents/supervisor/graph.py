from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing_extensions import Literal

from .prompts import INTENT_CLASSIFICATION_PROMPT
from .state import AgentState

load_dotenv()

model = "gpt-4o-mini"
agent = ChatOpenAI(model=model, temperature=0.0, max_tokens=500)

class IntentClassifier(BaseModel):
    user_intent: Literal["account", "transaction", "unknown"] = Field(
        ...,
        description='Classify whether the user wants to request information about their credit limit (account), check their latest transactions (transaction), or if the intent is unknown (unknown).'
    )
    
def supervisor(state: AgentState) -> AgentState:
    if not state.get("query") or not isinstance(state["query"], str) or not state["query"].strip():
        state["intent"] = "unknown"
        state["confidence"] = 0.0
        print("[Intent classifier] No valid query provided")
        return state

    intent_cls_llm = agent.with_structured_output(IntentClassifier)

    try:
        intent_result = intent_cls_llm.invoke([
            {
                "role": "system",
                "content": INTENT_CLASSIFICATION_PROMPT
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

