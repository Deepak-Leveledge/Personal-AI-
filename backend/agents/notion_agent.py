from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from state.agent_state import AgentState
from my_mcp.mcp_client import get_mcp_client
import asyncio
from dotenv import load_dotenv
load_dotenv()
import json
import os

## Initialize the Gemeni API client
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=os.getenv("GEMINI_API_KEY"))


@traceable(name="Notion Agent")
def notion_agent(state: AgentState) -> AgentState:
    # ✅ result ko variable mein pakdo
    result = asyncio.run(_notion_agent_async(state))
    return result

async def _notion_agent_async(state: AgentState) -> AgentState:
    print("\n📝 Notion Agent running...")
    state["status_updates"].append("📝 Checking Notion...")

    question = state["user_message"]

    try:
        client    = get_mcp_client()
        all_tools = await client.get_tools()

        # ✅ Notion tools = API- se start hote hain
        notion_tools = [
            t for t in all_tools
            if t.name.startswith("API-")
        ]

        print(f"📝 Notion tools found: {len(notion_tools)}")

        if not notion_tools:
            state["notion_result"] = (
                "Notion is not connected. "
                "Please add NOTION_API_KEY to .env"
            )
            return state

        print(f"📝 Tools: {[t.name for t in notion_tools]}")

        # ── decide which tool ───────────────────
        tools_desc = "\n".join([
            f"- {t.name}: {t.description[:100]}"
            for t in notion_tools
        ])

        decide_prompt = f"""
        You are a Notion assistant.
        User request: {question}

        Available Notion tools:
        {tools_desc}

        Which tool should be used and with what input?
        Reply in EXACTLY this format:
        TOOL: <exact tool name>
        INPUT: <valid JSON input for the tool>

        Common tool usage:
        - Search anything  → API-post-search
          INPUT: {{"query": "search term"}}

        - Read a page      → API-retrieve-a-page
          INPUT: {{"page_id": "page-id-here"}}

        - Query database   → API-query-data-source
          INPUT: {{"database_id": "db-id-here"}}

        Always start with API-post-search for
        any search request.
        Return ONLY TOOL and INPUT lines. Nothing else.
        """

        decision      = llm.invoke(decide_prompt)
        decision_text = decision.content.strip()
        print(f"🤖 Decision:\n{decision_text}")

        # ── parse ────────────────────────────────
        tool_name  = None
        tool_input = {}

        for line in decision_text.split("\n"):
            line = line.strip()
            if line.startswith("TOOL:"):
                tool_name = line.replace(
                    "TOOL:", ""
                ).strip()
            if line.startswith("INPUT:"):
                try:
                    raw        = line.replace(
                        "INPUT:", ""
                    ).strip()
                    tool_input = json.loads(raw)
                except:
                    tool_input = {}

        print(f"🔧 Tool : {tool_name}")
        print(f"🔧 Input: {tool_input}")

        if not tool_name:
            state["notion_result"] = (
                "Could not determine Notion action."
            )
            return state

        # ── find tool ────────────────────────────
        tool = next(
            (t for t in notion_tools
             if t.name == tool_name),
            None
        )

        if not tool:
            tool = next(
                (t for t in notion_tools
                 if tool_name.lower()
                 in t.name.lower()),
                None
            )

        if not tool:
            state["notion_result"] = (
                f"Tool '{tool_name}' not found.\n"
                f"Available: "
                f"{[t.name for t in notion_tools]}"
            )
            return state

        # ── run tool ─────────────────────────────
        print(f"⚡ Running: {tool.name}")
        raw_result = await tool.ainvoke(tool_input)
        print("✅ Notion result received!")

        # ── summarize ────────────────────────────
        summarize_prompt = f"""
        You are a helpful Notion assistant.
        User asked: {question}

        Raw Notion data:
        {str(raw_result)[:5000]}

        Provide a clean helpful response.
        Format pages as numbered list with titles.
        Be concise and clear.
        """

        summary                = llm.invoke(summarize_prompt)
        state["notion_result"] = summary.content.strip()
        state["status_updates"].append(
            "✅ Notion data retrieved!"
        )

    except Exception as e:
        print(f"❌ Notion Agent error: {e}")
        state["notion_result"] = (
            f"Could not access Notion: {str(e)}"
        )
        state["error"] = str(e)

    print("✅ Notion Agent done!")
    return state