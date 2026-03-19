from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from state.agent_state import AgentState
from my_mcp.mcp_client import get_mcp_client
import asyncio
import json
import os



## Initialize the Gemeni API client
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=os.getenv("GEMINI_API_KEY"))



@traceable(name="GitHub Agent")
def github_agent(state: AgentState) -> AgentState:
    return asyncio.run(_github_agent_async(state))

async def _github_agent_async(state: AgentState) -> AgentState:
    print("\n🐙 GitHub Agent running...")
    state["status_updates"].append("🐙 Checking GitHub...")

    question = state["user_message"]

    try:
        client    = get_mcp_client()
        all_tools = await client.get_tools()

        github_tools = [
            t for t in all_tools
            if not t.name.startswith("API-")
        ]

        if not github_tools:
            state["github_result"] = (
                "GitHub is not connected."
            )
            return state

        print(f"🐙 Available GitHub tools: "
              f"{[t.name for t in github_tools]}")

        tools_desc = "\n".join([
            f"- {t.name}: {t.description[:100]}"
            for t in github_tools
        ])

        github_user = os.getenv(
            "GITHUB_USERNAME", ""
        ).strip()

        decide_prompt = f"""
        You are a GitHub assistant.
        User request: {question}
        GitHub username: {github_user}

        Available GitHub tools:
        {tools_desc}

        Which tool should be used and with what input?
        Reply in EXACTLY this format:
        TOOL: <exact tool name>
        INPUT: <valid JSON input for the tool>

        IMPORTANT input examples:
        - search_repositories → {{"query": "user:{github_user}"}}
        - list_issues → {{"owner": "{github_user}", "repo": "repo_name", "state": "open"}}
        - list_commits → {{"owner": "{github_user}", "repo": "repo_name"}}
        - search_code → {{"query": "language:python user:{github_user}"}}
        - list_pull_requests → {{"owner": "{github_user}", "repo": "repo_name", "state": "open"}}

        For listing MY repos use:
        search_repositories with query "user:{github_user}"

        Return ONLY the TOOL and INPUT lines nothing else.
        """

        decision      = llm.invoke(decide_prompt)
        decision_text = decision.content.strip()
        print(f"🤖 Tool decision:\n{decision_text}")

        tool_name  = None
        tool_input = {}

        for line in decision_text.split("\n"):
            line = line.strip()
            if line.startswith("TOOL:"):
                tool_name = line.replace("TOOL:", "").strip()
            if line.startswith("INPUT:"):
                try:
                    raw        = line.replace("INPUT:", "").strip()
                    tool_input = json.loads(raw)
                except:
                    tool_input = {}

        # ── fix common missing inputs ────────────
        if tool_name == "search_repositories":
            if not tool_input.get("query"):
                tool_input = {"query": f"user:{github_user}"}
                print(f"🔧 Fixed input: {tool_input}")

        print(f"🔧 Tool : {tool_name}")
        print(f"🔧 Input: {tool_input}")

        if not tool_name:
            state["github_result"] = (
                "Could not determine GitHub action."
            )
            return state

        tool = next(
            (t for t in github_tools
             if t.name == tool_name),
            None
        )

        if not tool:
            tool = next(
                (t for t in github_tools
                 if tool_name.lower() in t.name.lower()),
                None
            )

        if not tool:
            state["github_result"] = (
                f"Tool '{tool_name}' not found."
            )
            return state

        print(f"⚡ Running: {tool.name}")
        raw_result = await tool.ainvoke(tool_input)
        print("✅ GitHub tool result received!")

        summarize_prompt = f"""
        You are a helpful GitHub assistant.
        User asked: {question}

        Raw GitHub data:
        {str(raw_result)[:5000]}

        Provide a clean helpful response.
        Format repos and issues as a numbered list.
        Be concise and clear.
        """

        summary                = llm.invoke(summarize_prompt)
        state["github_result"] = summary.content.strip()
        state["status_updates"].append(
            "✅ GitHub data retrieved!"
        )

    except Exception as e:
        print(f"❌ GitHub Agent error: {e}")
        state["github_result"] = (
            f"Could not access GitHub: {str(e)}"
        )
        state["error"] = str(e)

    print("✅ GitHub Agent done!")
    return state