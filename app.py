import streamlit as st
from langgraph_comparison import app, AutomationState

st.title("Pipedrive Automation Parser")
st.write("Describe an automation in plain English and I'll convert it to a structured format.")

# Initialize session state
if "result" not in st.session_state:
    st.session_state.result = None
if "needs_clarification" not in st.session_state:
    st.session_state.needs_clarification = False
if "original_input" not in st.session_state:
    st.session_state.original_input = ""

user_input = st.text_input("What should be automated?",
                            placeholder="e.g. when a deal moves to closed won, send me a Slack message")

if st.button("Parse Automation") and user_input:
    # Check for ambiguity before running the graph
    if "big" in user_input or "top" in user_input:
        st.session_state.needs_clarification = True
        st.session_state.original_input = user_input
    else:
        result = app.invoke({
            "user_input": user_input,
            "intent": "",
            "warning": "",
            "clarification": "",
            "ready": False
        })
        st.session_state.result = result
        st.session_state.needs_clarification = False

# Show clarification input if needed
if st.session_state.needs_clarification:
    st.warning("⚠️ Your request contains an ambiguous qualifier.")
    clarification = st.text_input("Please clarify — e.g. 'over $50k'")
    if st.button("Submit Clarification") and clarification:
        full_input = st.session_state.original_input + " " + clarification
        result = app.invoke({
            "user_input": full_input,
            "intent": "",
            "warning": "",
            "clarification": clarification,
            "ready": False
        })
        st.session_state.result = result
        st.session_state.needs_clarification = False

# Show result
if st.session_state.result:
    st.subheader("Result")
    st.json(st.session_state.result)