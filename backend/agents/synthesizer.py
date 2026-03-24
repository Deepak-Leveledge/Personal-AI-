from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from state.agent_state import AgentState
import os


## Initialize the Gemeni API client
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=os.getenv("GEMINI_API_KEY"))

@traceable(name="Response Synthesizer")
def synthesizer_agent(state: AgentState) -> AgentState:
    print("\n🔗 Response Synthesizer running...")

    question = state["user_message"]
    agents   = state.get("agents_to_run", ["general"])
    messages = state.get("messages", [])

    # ── collect all agent results ───────────────
    results = {}

    if state.get("rag_result"):
        results["Documents"] = state["rag_result"]

    if state.get("web_result"):
        results["Web Search"] = state["web_result"]

    if state.get("github_result"):
        results["GitHub"] = state["github_result"]

    if state.get("notion_result"):
        results["Notion"] = state["notion_result"]

    # ── if only general — answer directly ───────
    if agents == ["general"] and not results:
        print("💬 General question — answering directly")

        history = ""
        if messages:
            last    = messages[-6:] if len(messages) >= 6 else messages
            history = "\n".join(
                [f"{m['role']}: {m['content']}"
                 for m in last]
            )

        prompt = f"""
You are a helpful, smart, and knowledgeable AI assistant.

Your job is to first understand the user's intent and then respond in the most appropriate way.

Behavior rules:
- If the user is greeting you (like "hi", "hello", "hey"), respond warmly and briefly in 1 short line.
- If the user is thanking you, respond politely and briefly.
- If the user asks a simple or casual question, give a short and direct answer.
- If the user asks a complex, technical, or explanatory question, give a clear, detailed, and well-structured answer.
- Do not give long explanations when the user only wants a short reply.
- Use headings, bullet points, and markdown only when they actually improve readability.
- Keep your tone natural, helpful, and conversational.
- Do not sound robotic or unnecessarily verbose.

Identity:
- You are a helpful AI assistant.

Chat history:
{history}

User question:
{question}

Now generate the best response based on the user's intent and query complexity.
"""


        response             = llm.invoke(prompt)
        state["final_answer"] = response.content.strip()
        print("✅ General answer generated!")
        return state

    # ── if no results from any agent ────────────
    if not results:
        state["final_answer"] = (
            "I could not find relevant information "
            "to answer your question. "
            "Please try rephrasing or check your "
            "connected services."
        )
        return state

    # ── combine multiple agent results ──────────
    results_text = ""
    for source, content in results.items():
        results_text += f"\n[{source}]\n{content}\n---"

    history = ""
    if messages:
        last    = messages[-4:] if len(messages) >= 4 else messages
        history = "\n".join(
            [f"{m['role']}: {m['content']}"
             for m in last]
        )

    # single agent — just clean and present
    if len(results) == 1:
        source, content = list(results.items())[0]

        prompt = f"""
        You are a helpful personal AI assistant.
        Present this information cleanly to the user.

        User asked: {question}

        Information from {source}:
        {content}

        Chat history:
        {history}

        Rules:
        - Be concise and clear
        - Format nicely
        - Directly answer the question
        - Do not add unnecessary filler
        """

    else:
        # multiple agents — synthesize together
        prompt = f"""
        You are a helpful personal AI assistant.
        Synthesize information from multiple sources
        into one clear coherent answer.

        User asked: {question}

        Information from agents:
        {results_text}

        Chat history:
        {history}

        Rules:
        - Combine all sources naturally
        - Be concise and clear
        - Format nicely
        - Directly answer the question
        - Mention which source each part came from
        
        """

    response             = llm.invoke(prompt)
    state["final_answer"] = response.content.strip()

    state["status_updates"].append("✅ Answer ready!")
    print("✅ Response Synthesizer done!")
    return state