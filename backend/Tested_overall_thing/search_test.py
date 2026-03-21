from dotenv import load_dotenv
import os
load_dotenv()
from agents.web_search_agent import web_search_agent
from state.agent_state import AgentState


def make_state(message: str) -> AgentState:
    return {
        "user_id"          : "deepak_001",
        "messages"         : [],
        "user_message"     : message,
        "is_safe"          : True,
        "block_reason"     : None,
        "intent"           : "websearch",
        "agents_to_run"    : ["websearch"],
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

# test 1 — current news
print("\n--- Test 1: Current news ---")
state = make_state("What are the latest developments in AI agents? and which companies are leading the way?")
state = web_search_agent(state)
print("\n========== WEB RESULT ==========")
print(state["web_result"])

# test 2 — factual question
print("\n--- Test 2: Factual question ---")
state = make_state("What is the current version of LangGraph? and how can I integrate Google Gmail MCP in the on project?")
state = web_search_agent(state)
print("\n========== WEB RESULT ==========")
print(state["web_result"])
