from langgraph.graph import StateGraph, END
from state.agent_state import AgentState
from guardrails.input_guard import input_guard
from agents.supervisor_agent import supervisor_agent
from agents.rag_agent import rag_agent
from agents.web_search_agent import web_search_agent
from agents.github_agent import github_agent
from agents.notion_agent import notion_agent
# from agents.gmail_agent import gmail_agent
from agents.synthesizer import synthesizer_agent
import asyncio


# ── Conditional edge — guardrail ────────────────
def check_guardrail(state: AgentState) -> str:
    if not state.get("is_safe", True):
        print("🚫 Message blocked by guardrail")
        return "blocked"
    return "safe"

# ── Conditional edge — route agents ─────────────
def route_agents(state: AgentState) -> str:
    agents = state.get("agents_to_run", ["general"])
    print(f"🔀 Routing to agents: {agents}")

    if agents == ["general"]:
        return "general"
    elif agents == ["rag"]:
        return "rag"
    elif agents == ["websearch"]:
        return "websearch"
    elif agents == ["github"]:
        return "github"
    elif agents == ["notion"]:
        return "notion"
    else:
        return "parallel"

# ── Blocked node ─────────────────────────────────
def blocked_node(state: AgentState) -> AgentState:
    print("🚫 Request blocked")
    return state


# ── Parallel agents node ─────────────────────────
def parallel_agents_node(state: AgentState) -> AgentState:
    print("\n⚡ Running agents in parallel...")

    agents  = state.get("agents_to_run", [])
    tasks   = []

    async def run_all():
        loop    = asyncio.get_event_loop()
        futures = []

        if "rag" in agents:
            futures.append(
                loop.run_in_executor(None, rag_agent, state.copy())
            )
        if "websearch" in agents:
            futures.append(
                loop.run_in_executor(
                    None, web_search_agent, state.copy()
                )
            )
        if "github" in agents:
            futures.append(
                loop.run_in_executor(
                    None, github_agent, state.copy()
                )
            )
        if "notion" in agents:
            futures.append(
                loop.run_in_executor(
                    None, notion_agent, state.copy()
                )
            )

        results = await asyncio.gather(*futures)
        return results

    try:
        results = asyncio.run(run_all())

        # merge results back into main state
        for result in results:
            if result.get("rag_result"):
                state["rag_result"] = result["rag_result"]
            if result.get("web_result"):
                state["web_result"] = result["web_result"]
            if result.get("github_result"):
                state["github_result"] = result["github_result"]
            if result.get("notion_result"):
                state["notion_result"] = result["notion_result"]

        print("✅ All parallel agents done!")

    except Exception as e:
        print(f"❌ Parallel execution error: {e}")
        state["error"] = str(e)

    return state



# ── Build main graph ─────────────────────────────
def build_main_graph():
    graph = StateGraph(AgentState)

    # add all nodes
    graph.add_node("input_guardrail",   input_guard)
    graph.add_node("supervisor",        supervisor_agent)
    graph.add_node("blocked",           blocked_node)
    # graph.add_node("general",           general_node)
    graph.add_node("rag",               rag_agent)
    graph.add_node("websearch",         web_search_agent)
    graph.add_node("github",            github_agent)
    graph.add_node("notion",            notion_agent)
    graph.add_node("parallel_agents",   parallel_agents_node)
    graph.add_node("synthesizer",       synthesizer_agent)

    # entry point
    graph.set_entry_point("input_guardrail")

    # guardrail → safe or blocked
    graph.add_conditional_edges(
        "input_guardrail",
        check_guardrail,
        {
            "blocked" : "blocked",
            "safe"    : "supervisor"
        }
    )

    # blocked → END
    graph.add_edge("blocked", END)

    # supervisor → route to correct agent
    graph.add_conditional_edges(
        "supervisor",
        route_agents,
        {
            "general"  : "synthesizer",
            "rag"      : "rag",
            "websearch": "websearch",
            "github"   : "github",
            "notion"   : "notion",
            "parallel" : "parallel_agents"
        }
    )

    # all agents → synthesizer
    # graph.add_edge("general",         "synthesizer")
    graph.add_edge("rag",             "synthesizer")
    graph.add_edge("websearch",       "synthesizer")
    graph.add_edge("github",          "synthesizer")
    graph.add_edge("notion",          "synthesizer")
    graph.add_edge("parallel_agents", "synthesizer")

    # synthesizer → END
    graph.add_edge("synthesizer", END)

    return graph.compile()