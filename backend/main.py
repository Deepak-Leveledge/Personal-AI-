from dotenv import load_dotenv
from state.agent_state import AgentState
import os
load_dotenv()


# keys = {
#     "GEMINI"    : os.getenv("GEMINI_API_KEY"),
#     "LANGSMITH" : os.getenv("LANGSMITH_API_KEY"),
#     "TAVILY"    : os.getenv("TAVILY_API_KEY"),
#     "PINECONE"  : os.getenv("PINECONE_API_KEY"),
#     "MONGODB"   : os.getenv("MONGODB_URI"),
# }


# print("================================")
# for name,value in keys.items():
#     status = "✅" if value else "❌ MISSING"
#     preview = value[:6] + "..." if value else "not set"
#     print(f"{status}  {name}: {preview}")
# print("================================")



# create a test state
test_state: AgentState = {
    "messages": [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi! How can I help?"},
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi! How can I help?"},
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi! How can I help?"},
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi! How can I help?"}
    ],
    "user_message": "Summarize my PDF",

    "is_safe": None,
    "block_reason": None,

    "intent": None,
    "agents_to_run": None,

    "rag_result": None,
    "web_result": None,
    "gmail_result": None,
    "calendar_result": None,
    "notion_result": None,
    "github_result": None,

    "rewritten_query": None,
    "retrieved_chunks": None,
    "reranked_chunks": None,
    "rag_is_relevant": None,
    "is_hallucination": None,

    "status_updates": [],
    "current_status": None,

    "final_answer": None,
    "sources": None,    
    "error": None,
}

print("✅ Agent State created successfully!")
print(f"Messages in history : {len(test_state['messages'])}")
print(f"Current message     : {test_state['user_message']}")
print(f"All agent outputs   : None — ready for agents to fill!")