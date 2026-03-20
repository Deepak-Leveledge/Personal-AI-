from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from state.agent_state import AgentState
import os
from dotenv import load_dotenv
load_dotenv()


## Initialize the Gemeni API client
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=os.getenv("GEMINI_API_KEY"))


# ── All possible intents ────────────────────────
INTENTS = {
    "general"  : "General knowledge question — answer directly",
    "rag"      : "Question about uploaded documents or files",
    "websearch": "Needs current/realtime web information",
    "github"   : "GitHub repos, issues, PRs, code",
    "notion"   : "Notion pages, databases, notes",
    "mixed"    : "Needs multiple agents together",
}

@traceable(name="Supervisor Agent")
def supervisor_agent(state: AgentState) -> AgentState:
    print("\n🧠 Supervisor Agent running...")

    message  = state["user_message"]
    messages = state.get("messages", [])

    # build recent chat history for context
    history = ""
    if messages:
        last    = messages[-4:] if len(messages) >= 4 else messages
        history = "\n".join(
            [f"{m['role']}: {m['content']}" for m in last]
        )

    intents_desc = "\n".join(
        [f"- {k}: {v}" for k, v in INTENTS.items()]
    )

    prompt = f"""
    You are a smart AI assistant router.
    Analyze the user message and decide which
    agents should handle it.

    Available intents:
    {intents_desc}

    Rules:
    - "general"   → simple knowledge questions
                    no tools needed
                    Example: "what is python?"

    - "rag"       → user asks about their documents
                    keywords: my pdf, my document,
                    summarize, in my file, from my doc
                    Example: "summarize my pdf"

    - "websearch" → needs current information
                    keywords: latest, current, today,
                    news, price, weather, recent
                    Example: "latest AI news"

    - "github"    → anything about GitHub
                    keywords: repo, issue, PR, commit,
                    code, github, pull request
                    Example: "show my repos"

    - "notion"    → anything about Notion
                    keywords: notion, page, database,
                    notes, workspace
                    Example: "search my notion"

    - "mixed"     → needs 2 or more agents
                    Example: "search web and save to notion"
                    Example: "check github issues and
                               search web for solution"

    Chat history:
    {history}

    User message: {message}

    Reply in EXACTLY this format:
    INTENT: <single intent from list above>
    AGENTS: <comma separated agents to run>
    REASON: <one line why>

    For AGENTS use these exact names:
    rag, websearch, github, notion, general

    Examples:
    INTENT: general
    AGENTS: general
    REASON: Simple factual question needs no tools

    INTENT: rag
    AGENTS: rag
    REASON: User asking about their uploaded document

    INTENT: mixed
    AGENTS: websearch, github
    REASON: Needs web search and GitHub data together
    """

    response = llm.invoke(prompt)
    result   = response.content.strip()
    print(f"🧠 Supervisor decision:\n{result}")

    # ── parse intent and agents ─────────────────
    intent      = "general"
    agents      = ["general"]
    reason      = ""

    for line in result.split("\n"):
        line = line.strip()
        if line.startswith("INTENT:"):
            intent = line.replace(
                "INTENT:", ""
            ).strip().lower()
        if line.startswith("AGENTS:"):
            raw    = line.replace("AGENTS:", "").strip()
            agents = [
                a.strip().lower()
                for a in raw.split(",")
                if a.strip()
            ]
        if line.startswith("REASON:"):
            reason = line.replace("REASON:", "").strip()

    # ── validate agents ─────────────────────────
    valid_agents = {"rag", "websearch", "github",
                    "notion", "general"}
    agents = [a for a in agents if a in valid_agents]

    # fallback if no valid agents
    if not agents:
        agents = ["general"]
        intent = "general"

    state["intent"]       = intent
    state["agents_to_run"] = agents
    state["status_updates"].append(
        f"🧠 Routing to: {', '.join(agents)}"
    )

    print(f"✅ Intent : {intent}")
    print(f"✅ Agents : {agents}")
    print(f"✅ Reason : {reason}")
    return state
