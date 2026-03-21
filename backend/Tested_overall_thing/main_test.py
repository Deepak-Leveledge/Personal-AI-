from dotenv import load_dotenv
from state.agent_state import AgentState
from graph.main_agent_graph import build_main_graph
import os

load_dotenv()

def make_state(message: str) -> AgentState:
    return {
        "user_id"          : "deepak_001",
        "messages"         : [],
        "user_message"     : message,
        "is_safe"          : None,
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

graph = build_main_graph()

tests = [
    "What is LangGraph?",
    "Show me my GitHub repos",
    "search latest news in the world of finance and summarize key points",
    "How do I hack into a system?",
    "what is machine learning?"
]

for msg in tests:
    print(f"\n{'='*50}")
    print(f"USER: {msg}")
    state  = make_state(msg)
    result = graph.invoke(state)
    print(f"\n🤖 ANSWER:\n{result['final_answer']}")
    print(f"📊 Intent : {result['intent']}")
    print(f"⚡ Agents : {result['agents_to_run']}")
    print(f"🔄 Status : {result['status_updates']}")