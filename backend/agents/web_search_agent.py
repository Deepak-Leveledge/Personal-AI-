from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from state.agent_state import AgentState
from dotenv import load_dotenv
from tools.search_tool import search_web

import os
load_dotenv()

## Initialize the Gemeni API client
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=os.getenv("GEMINI_API_KEY"))


@traceable(name="web_search_agent")
def web_search_agent(state:AgentState) ->AgentState:
    print("🔎 Running Web Search Agent...")

    question = state["user_message"]
    state["status_updates"].append("🌐 Searching the web...")

    # step 1 — rewrite query for better search
    rewrite_prompt = f"""
    Convert this question into a short web search query.
    Max 8 to 10words. No filler words.
    Return ONLY the query nothing else.

    Question: {question}
    """
    rewritten = llm.invoke(rewrite_prompt).content.strip()
    print(f"🔍 Search query: {rewritten}")

    # step 2 — search the web
    raw_results =search_web(
        query= rewritten,
        num_results=5
    )


    if not raw_results:
        state["web_result"] = (
            "I could not find any relevant "
            "web results for your question."
        )
        print("❌ No web results found")
        return state
    

    #step 3 Summirize search results jo mila hai

    summarize_prompt = f"""
    You are a helpful assistant.
    Answer the user question using the web search
    results below.

    Rules:
    - Be concise and clear
    - Only use info from the search results
    - Mention sources where relevant
    - If results are not relevant say so

    User question: {question}

    Search results:
    {raw_results}
    """

    response           = llm.invoke(summarize_prompt)
    print(f"✅ Web search summary:\n{response.content.strip()}")
    state["web_result"] = response.content.strip()
    state["status_updates"].append("✅ Web search complete!")

    print("✅ Web Search Agent done!")
    return state
