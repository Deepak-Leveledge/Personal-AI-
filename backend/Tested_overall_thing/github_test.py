from dotenv import load_dotenv
from state.agent_state import AgentState
from agents.github_agent import github_agent
import os

load_dotenv()

def make_state(message: str) -> AgentState:
    return {
        "user_id"          : "deepak_001",
        "messages"         : [],
        "user_message"     : message,
        "is_safe"          : True,
        "block_reason"     : None,
        "intent"           : "github",
        "agents_to_run"    : ["github"],
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

# test 1 — list repos
print("\n--- Test 1: List my repos ---")
state = make_state("Show me my GitHub repositories")
state = github_agent(state)
print("\n========== GITHUB RESULT ==========")
print(state["github_result"])

# test 2 — list issues
print("\n--- Test 2: List issues ---")
state = make_state(
    "create new repo with the name testing github mcp"
)
state = github_agent(state)
print("\n========== GITHUB RESULT ==========")
print(state["github_result"])