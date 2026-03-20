from dotenv import load_dotenv
from state.agent_state import AgentState
from agents.supervisor_agent import supervisor_agent
import os

load_dotenv()

def make_state(message: str) -> AgentState:
    return {
        "user_id"          : "deepak_001",
        "messages"         : [],
        "user_message"     : message,
        "is_safe"          : True,
        "block_reason"     : None,
        "intent"           : None,
        "agents_to_run"    : None,
        "rag_result"       : None,
        "web_result"       : None,
        "gmail_result"     : None,
        "calendar_result"  : None,
        "notion_result"    : None,
        "github_result"    : None,
        "rewritten_query"  : None,
        "retrieved_chunks" : None,
        "reranked_chunks"  : None,
        "rag_is_relevant"  : None,
        "is_hallucination" : None,
        "rag_retry_count"  : 0,
        "status_updates"   : [],
        "current_status"   : None,
        "final_answer"     : None,
        "sources"          : None,
        "error"            : None,
    }

tests = [
    "What is machine learning?",
    "Summarize my uploaded PDF",
    "What are the latest AI news today?",
    "Show me my GitHub repositories",
    "Search my Notion for project notes",
    "Search web for LangGraph summarize the key points and give me a concise answer",
]

for msg in tests:
    print(f"\n{'='*45}")
    print(f"Message : {msg}")
    state = make_state(msg)
    state = supervisor_agent(state)
    print(f"Intent  : {state['intent']}")
    print(f"Agents  : {state['agents_to_run']}")