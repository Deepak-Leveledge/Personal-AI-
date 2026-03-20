from dotenv import load_dotenv
from state.agent_state import AgentState
from agents.notion_agent import notion_agent
import os

load_dotenv()

def make_state(message: str) -> AgentState:
    return {
        "user_id"          : "deepak_001",
        "messages"         : [],
        "user_message"     : message,
        "is_safe"          : True,
        "block_reason"     : None,
        "intent"           : "notion",
        "agents_to_run"    : ["notion"],
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

# test 1 — search pages
print("\n--- Test 1: Search Notion pages ---")
state = make_state("Search my Notion and tell me what is there in the page")
state = notion_agent(state)
print("\n========== NOTION RESULT ==========")
print(state["notion_result"])

# test 2 — general search
print("\n--- Test 2: Search anything ---")
state = make_state("What pages do I have in Notion?")
state = notion_agent(state)
print("\n========== NOTION RESULT ==========")
print(state["notion_result"])

# test 2 — general search
print("\n--- Test 3: Search anything ---")
state = make_state("make a new page in Notion with the title test page and content this is a test page created by my AI assistant")
state = notion_agent(state)
print("\n========== NOTION RESULT ==========")
print(state["notion_result"])