from dotenv import load_dotenv
load_dotenv()
import asyncio
from state.agent_state import AgentState
from agents.gmail_agent import gmail_agent


state: AgentState = {
    "user_id"          : "deepak_001",
    "messages"         : [],
    "user_message"     : "Show me my last 5 unread emails",
    "is_safe"          : True,
    "block_reason"     : None,
    "intent"           : "gmail",
    "agents_to_run"    : ["gmail"],
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

state = gmail_agent(state)

print("\n========== GMAIL RESULT ==========")
print(state["gmail_result"])
print("\n========== STATUS UPDATES ==========")
print(state["status_updates"])