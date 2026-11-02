
from langgraph.graph import StateGraph, START, END
from state import InsightState

from tools import (
    data_query_tool,
    calculator_tool,
    chart_tool
)

from dotenv import load_dotenv
from langchain_groq import ChatGroq
import json

load_dotenv()

# INITIALIZE LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# NODE 1: PLANNING NODE

def planning_node(state: InsightState):

    question = state["question"].lower()
    selected_tools = state.get("selected_tools", [])

    # FOLLOW-UP WHY QUESTION
    if (
        "why" in question
        or "performing better" in question
    ):
        plan = """
        1. data_query – Retrieve revenue totals for each region.
        2. Compare West region revenue with other regions.
        3. Explain that the dataset shows revenue differences
           but cannot establish the root cause.
        """

    # AVERAGE QUESTION
    elif "average" in question:

        metric = state.get("metric") or "Revenue"

        plan = f"""
        1. data_query – Retrieve total {metric} and valid record count.
        2. calculator – Divide the total by the valid record count
           to calculate average {metric}.
        """

    # CHART QUESTION
    elif "chart" in question or "graph" in question:

        plan = """
        1. data_query – Group the requested metric by the selected category.
        2. chart – Generate a Plotly visualization from the grouped data.
        """

    # NORMAL DATA QUERY
    else:

        plan = f"""
        1. data_query – Retrieve the relevant information
           from the sales dataset.
        2. Analyze the returned results to answer the question.
        """

    return {
        "plan": plan
    }

# NODE 2: TOOL SELECTION NODE

def tool_selection_node(state: InsightState):

    question = state["question"]
    question_lower = question.lower()

    conversation_history = state.get("conversation_history", [])

    history_text = "\n".join(
        f'{message["role"]}: {message["content"]}'
        for message in conversation_history
    )

    history_lower = history_text.lower()

    # FOLLOW-UP CONTEXT RESOLUTION
    is_why_followup = (
        "why" in question_lower
        or "performing better" in question_lower
        or "better" in question_lower
    )

    previous_region_context = (
        "highest revenue" in history_lower
        or "which region" in history_lower
        or "revenue by region" in history_lower
    )
    
    # If the user asks why a previously identified region is performing better
    if is_why_followup and previous_region_context:
    
        
        return {
        "selected_tools": ["data_query"],
        "group_by": "Region",
        "metric": "Revenue",
        "operation": None
    }

    # NORMAL TOOL SELECTION
    prompt = f"""
    You are a tool selection assistant.

    Available tools:
    1. data_query
    2. calculator
    3. chart

    Previous conversation:
    {history_text}

    User question:
    {question}

    Select only the tools required.

    Return ONLY valid JSON in this format:
    {{
        "tools": ["data_query"],
        "group_by": null,
        "metric": "Revenue",
        "operation": null
    }}

    Rules:
    - Use data_query for dataset questions.
    - Use calculator for mathematical calculations.
    - Use calculator for average, percentage and division.
    - For average revenue, select data_query and calculator.
    - For average profit, select data_query and calculator.
    - Use chart for chart, graph or visualization requests.
    - For region-wise questions, group_by must be Region.
    - For product-wise questions, group_by must be Product.
    - metric must be Revenue, Profit or Units_Sold.
    - For average revenue, operation must be average.
    - For average profit, operation must be average.
    - For follow-up questions, use previous conversation to understand context.
    - Never select unnecessary tools.
    - Do not include Markdown code fences.
    """

    response = llm.invoke(prompt)

    try:
        content = response.content.strip()

        if content.startswith("```"):
            content = content.replace("```json", "")
            content = content.replace("```", "").strip()

        selection = json.loads(content)

    except Exception:
        selection = {
            "tools": ["data_query"],
            "group_by": None,
            "metric": "Revenue",
            "operation": None
        }

    allowed_tools = ["data_query", "calculator", "chart"]

    selected_tools = [
        tool for tool in selection.get("tools", [])
        if tool in allowed_tools
    ]

    if not selected_tools:
        selected_tools = ["data_query"]

    allowed_metrics = ["Revenue", "Profit", "Units_Sold"]

    metric = selection.get("metric", "Revenue")

    if metric not in allowed_metrics:
        metric = "Revenue"

    allowed_groups = ["Region", "Product"]

    group_by = selection.get("group_by")

    if group_by not in allowed_groups:
        group_by = None

    return {
        "selected_tools": selected_tools,
        "group_by": group_by,
        "metric": metric,
        "operation": selection.get("operation")
    }



# NODE 3: TOOL EXECUTION NODE

def tool_execution_node(state: InsightState):

    selected_tools = state["selected_tools"]

    group_by = state.get("group_by")
    metric = state.get("metric") or "Revenue"
    operation = state.get("operation")

    results = []

    for tool in selected_tools:

        # DATA QUERY TOOL
        if tool == "data_query":

            if group_by:
                result = data_query_tool(
                    query_type="group",
                    group_by=group_by,
                    metric=metric
                )
            else:
                result = data_query_tool()

            results.append({
                "tool": "data_query",
                "result": result
            })

        # CALCULATOR TOOL
        elif tool == "calculator":

            summary = data_query_tool()

            if operation == "average" and metric == "Revenue":

                valid_count = summary["valid_revenue_records"]

                result = calculator_tool(
                    "divide",
                    [
                        summary["total_revenue"],
                        valid_count
                    ]
                )

            elif operation == "average" and metric == "Profit":

                valid_count = summary["valid_profit_records"]

                result = calculator_tool(
                    "divide",
                    [
                        summary["total_profit"],
                        valid_count
                    ]
                )

            else:
                result = "Requested calculation is not yet supported."

            results.append({
                "tool": "calculator",
                "operation": operation,
                "result": result
            })

        # CHART TOOL
        elif tool == "chart":

            chart_group = group_by or "Region"
            chart_metric = metric or "Revenue"

            chart_tool(chart_group, chart_metric)

            results.append({
                "tool": "chart",
                "result": f"{chart_metric} by {chart_group} chart created",
                "group_by": chart_group,
                "metric": chart_metric
            })

    return {
        "tool_results": results
    }


# NODE 4: FINAL ANSWER NODE
def answer_node(state: InsightState):

    question = state["question"]
    conversation_history = state.get("conversation_history", [])
    history_text = "\n".join(
    f'{message["role"]}: {message["content"]}'
    for message in conversation_history
)
    results = state["tool_results"]

    prompt = f"""
    You are an expert Data Analyst.
    
    Previous Conversation:
    {history_text}

    User Question:
    {question}

    Actual Tool Results:
    {results}

    Instructions:
    1. Answer clearly and concisely.
    2. Use exact supporting numbers from tool results.
    3. Explain why the result matters.
    4. Never invent data.
    5. Never assume a currency symbol.
    6. Format large numbers with commas.
    7. Do not recalculate values already calculated by tools.
    8. If data is unavailable, say so.
    9. Do not claim a chart was displayed unless the chart tool was used.
    10. Use previous conversation to understand follow-up questions.
    11. If the user asks "why", "compare it", or refers to a previous result, use that context.
    12. Do not invent reasons that are not supported by dataset results.
    13. Do not claim reasons such as higher demand,
    better marketing or larger customer base unless
    supported by actual tool results.
    14. If the dataset only provides revenue comparisons,
    clearly state that it cannot establish the root cause.

    Give a concise business insight.
    """

    response = llm.invoke(prompt)

    return {
        "final_answer": response.content
    }


# CONDITIONAL ROUTING
def route_tools(state: InsightState):

    if state["selected_tools"]:
        return "tool_execution"

    return "answer"


# BUILD LANGGRAPH
def build_graph():

    workflow = StateGraph(InsightState)

    workflow.add_node("planning", planning_node)
    workflow.add_node("tool_selection", tool_selection_node)
    workflow.add_node("tool_execution", tool_execution_node)
    workflow.add_node("answer", answer_node)

    workflow.add_edge(START, "tool_selection")
    workflow.add_edge("tool_selection", "planning")

    workflow.add_conditional_edges(
        "planning",
        route_tools,
        {
            "tool_execution": "tool_execution",
            "answer": "answer"
        }
    )

    workflow.add_edge("tool_execution", "answer")
    workflow.add_edge("answer", END)

    return workflow.compile()


graph_app = build_graph()