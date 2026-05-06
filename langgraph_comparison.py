from langgraph.graph import StateGraph, END
from typing import TypedDict

class AutomationState(TypedDict):
    user_input: str
    intent: str
    warning: str
    clarification: str
    ready: bool

# Node 1 - parse intent
def parse_intent(state: AutomationState) -> AutomationState:
    user_input = state["user_input"]
    if "won" in user_input or "closed" in user_input:
        intent = "trigger: deal won"
    else:
        intent = "trigger: unknown"
    return {**state, "intent": intent}

# Node 2 - check for ambiguity
def check_ambiguity(state: AutomationState) -> AutomationState:
    # If user already provided clarification, don't ask again
    if state["clarification"]:
        return {**state, "warning": "", "ready": True}
    
    if "big" in state["user_input"] or "top" in state["user_input"]:
        return {**state, "warning": "ambiguous qualifier", "ready": False}
    
    return {**state, "warning": "", "ready": True}

# Node 3 - ask for clarification
def ask_clarification(state: AutomationState) -> AutomationState:
    new_input = state["user_input"] + " " + state["clarification"]
    return {**state, "user_input": new_input, "ready": False}

# Node 4 - format final output
def format_output(state: AutomationState) -> AutomationState:
    print(f"\nFinal intent: {state['intent']}")
    print(f"Input used:   {state['user_input']}")
    return state

# Decision function - where do we go after checking ambiguity?
def route_after_check(state: AutomationState) -> str:
    if not state["ready"]:
        return "ask_clarification"
    return "format_output"

# Build the graph
graph = StateGraph(AutomationState)
graph.add_node("parse_intent", parse_intent)
graph.add_node("check_ambiguity", check_ambiguity)
graph.add_node("ask_clarification", ask_clarification)
graph.add_node("format_output", format_output)

graph.set_entry_point("parse_intent")
graph.add_edge("parse_intent", "check_ambiguity")
graph.add_conditional_edges("check_ambiguity", route_after_check)
graph.add_edge("ask_clarification", "parse_intent")
graph.add_edge("format_output", END)

app = graph.compile()

# Only run directly if executing this file, not when imported
if __name__ == "__main__":
    app.invoke({
        "user_input": "ping the team whenever we close a big one",
        "intent": "",
        "warning": "",
        "clarification": "",
        "ready": False
    })