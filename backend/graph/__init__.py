from state.agent_state import AgentState

def is_blocked(state: AgentState) -> str:
    if not state.get("is_safe", True):
        return "blocked"
    return "safe"