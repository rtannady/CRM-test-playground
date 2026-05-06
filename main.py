from langgraph.graph import StateGraph, END
from typing import TypedDict

# Define the state — what gets passed between nodes
class AutomationState(TypedDict):
    user_input: str
    parsed_intent: str

# Node 1 — takes raw input and extracts intent
def parse_intent(state: AutomationState) -> AutomationState:
    user_input = state["user_input"]
    # Simple rule for now — we'll replace this with an LLM call later
    if "won" in user_input or "closed" in user_input:
        intent = "trigger: deal won"
    elif "created" in user_input or "added" in user_input:
        intent = "trigger: record created"
    else:
        intent = "trigger: unknown — needs clarification"
    
    return {"user_input": user_input, "parsed_intent": intent}

# Node 2 — formats the output
def format_output(state: AutomationState) -> AutomationState:
    print(f"\nInput:  {state['user_input']}")
    print(f"Intent: {state['parsed_intent']}")
    return state

# Build the graph
graph = StateGraph(AutomationState)
graph.add_node("parse_intent", parse_intent)
graph.add_node("format_output", format_output)

graph.set_entry_point("parse_intent")
graph.add_edge("parse_intent", "format_output")
graph.add_edge("format_output", END)

app = graph.compile()

# Run it
result = app.invoke({"user_input": "when a deal moves to closed won, send me a Slack message"})