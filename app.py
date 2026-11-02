import streamlit as st
from graph import graph_app
from tools import chart_tool 

st.set_page_config(
    page_title="Insight Copilot",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Insight Copilot")
st.write("Your AI-powered Sales Data Analyst")

st.markdown("---")

# CHAT HISTORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# DISPLAY OLD MESSAGES
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message["role"] == "assistant":

            with st.expander("🧠 Show Reasoning Plan"):
                st.write(message["plan"])

            st.subheader("Final Answer")
            st.write(message["answer"])

            chart_info = message.get("chart")

            if chart_info:
                fig = chart_tool(
                    chart_info["group_by"],
                    chart_info["metric"]
                )
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.write(message["content"])

# NEW USER QUESTION
user_question = st.chat_input(
    "Ask anything about your sales data..."
)

if user_question:

    # Get previous conversation history
    conversation_history = [
    {
        "role": message["role"],
        "content": message.get(
            "content",
            message.get("answer", "")
        )
    }
    for message in st.session_state.messages
]
    
    # Save current user question
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    result = graph_app.invoke({
        "question": user_question,
        "conversation_history": conversation_history,
        "plan": "",
        "selected_tools": [],
        "group_by": None,
        "metric": None,
        "operation": None,
        "tool_results": [],
        "final_answer": ""
    })

    chart_info = next(
        (
            item for item in result["tool_results"]
            if item["tool"] == "chart"
        ),
        None
    )

    st.session_state.messages.append({
        "role": "assistant",
        "plan": result["plan"],
        "answer": result["final_answer"],
        "chart": chart_info
    })

    st.rerun()