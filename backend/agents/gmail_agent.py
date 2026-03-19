from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from state.agent_state import AgentState
from dotenv import load_dotenv
from my_mcp.mcp_client import get_mcp_client
import asyncio
import os
import json
load_dotenv()

## Initialize the Gemeni API client
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=os.getenv("GEMINI_API_KEY"))




def gmail_agent(state: AgentState) -> AgentState:
    print("⏭️ Gmail Agent — skipped for now")
    state["gmail_result"] = (
        "Gmail integration coming soon!"
    )
    return state

def calendar_agent(state: AgentState) -> AgentState:
    print("⏭️ Calendar Agent — skipped for now")
    state["calendar_result"] = (
        "Calendar integration coming soon!"
    )
    return state


# @traceable(name="Gmail Agent")
# def gmail_agent(state: AgentState) -> AgentState:
#     return asyncio.run(_gmail_agent_async(state))

# async def _gmail_agent_async(state: AgentState) -> AgentState:
#     print("\n📧 Gmail Agent running...")
#     state["status_updates"].append("📧 Checking your emails...")

#     question = state["user_message"]

#     try:
#         client = get_mcp_client()

#         # ✅ no async with — directly call get_tools()
#         all_tools   = await client.get_tools()
#         gmail_tools = [
#             t for t in all_tools
#             if "gmail" in t.name.lower()
#             or "email" in t.name.lower()
#             or "mail"  in t.name.lower()
#         ]

#         if not gmail_tools:
#             state["gmail_result"] = (
#                 "Gmail is not connected. "
#                 "Please check your credentials in .env"
#             )
#             return state

#         print(f"📧 Available Gmail tools: "
#               f"{[t.name for t in gmail_tools]}")

#         # ── decide which tool to use ────────────
#         tools_desc = "\n".join(
#             [f"- {t.name}: {t.description}"
#              for t in gmail_tools]
#         )

#         decide_prompt = f"""
#         You are a Gmail assistant.
#         User request: {question}

#         Available tools:
#         {tools_desc}

#         Which tool should be used and with what input?
#         Reply in EXACTLY this format:
#         TOOL: <tool_name>
#         INPUT: <json input for the tool>

#         Keep INPUT as valid JSON only.
#         """

#         decision      = llm.invoke(decide_prompt)
#         decision_text = decision.content.strip()
#         print(f"🤖 Tool decision:\n{decision_text}")

#         # ── parse tool name and input ───────────
#         tool_name  = None
#         tool_input = {}

#         for line in decision_text.split("\n"):
#             if line.startswith("TOOL:"):
#                 tool_name = line.replace("TOOL:", "").strip()
#             if line.startswith("INPUT:"):
#                 try:
#                     raw        = line.replace("INPUT:", "").strip()
#                     tool_input = json.loads(raw)
#                 except:
#                     tool_input = {}

#         if not tool_name:
#             state["gmail_result"] = (
#                 "Could not determine Gmail action."
#             )
#             return state

#         # ── find and run the tool ───────────────
#         tool = next(
#             (t for t in gmail_tools
#              if t.name == tool_name),
#             None
#         )

#         if not tool:
#             tool = next(
#                 (t for t in gmail_tools
#                  if tool_name.lower() in t.name.lower()),
#                 None
#             )

#         if not tool:
#             state["gmail_result"] = (
#                 f"Tool {tool_name} not found. "
#                 f"Available: {[t.name for t in gmail_tools]}"
#             )
#             return state

#         print(f"⚡ Running tool: {tool.name}")
#         raw_result = await tool.ainvoke(tool_input)
#         print("✅ Tool result received!")

#         # ── summarize with Gemini ───────────────
#         summarize_prompt = f"""
#         You are a helpful Gmail assistant.
#         User asked: {question}

#         Raw Gmail data:
#         {str(raw_result)[:2000]}

#         Provide a clean helpful response.
#         Format emails nicely if listing them.
#         Be concise and clear.
#         """

#         summary               = llm.invoke(summarize_prompt)
#         state["gmail_result"] = summary.content.strip()
#         state["status_updates"].append("✅ Emails retrieved!")

#     except Exception as e:
#         print(f"❌ Gmail Agent error: {e}")
#         state["gmail_result"] = f"Could not access Gmail: {str(e)}"
#         state["error"]        = str(e)

#     print("✅ Gmail Agent done!")
#     return state