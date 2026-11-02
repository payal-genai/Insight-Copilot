
# Insight Copilot – System Architecture

## Architecture Diagram

```mermaid
flowchart TB

    USER(["User"])
    UI["Streamlit Chat Interface"]

    subgraph LANGGRAPH["LangGraph StateGraph Workflow"]

        START(["START"])

        TS["Tool Selection Node"]
        PLAN["Planning Node"]

        ROUTE{"Conditional Routing"}

        EXEC["Tool Execution Node"]

        subgraph TOOLS["Available Python Tools"]
            DATA["Data Query Tool<br/>Pandas"]
            CALC["Calculator Tool<br/>Mathematical Operations"]
            CHART["Chart Tool<br/>Plotly Visualization"]
        end

        ANSWER["Answer Generation Node"]

        ENDNODE(["END"])

        START --> TS
        TS --> PLAN
        PLAN --> ROUTE

        ROUTE -->|"Tools Required"| EXEC
        ROUTE -->|"No Tools Required"| ANSWER

        EXEC --> DATA
        EXEC --> CALC
        EXEC --> CHART

        DATA --> ANSWER
        CALC --> ANSWER
        CHART --> ANSWER

        ANSWER --> ENDNODE
    end

    DATASET[("Cleaned Sales CSV Dataset")]

    LLM["Groq LLM<br/>openai/gpt-oss-120b"]

    USER --> UI
    UI --> START
    ENDNODE --> UI

    DATASET --> DATA

    LLM -.-> TS
    LLM -.-> PLAN
    LLM -.-> ANSWER

    classDef user fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef process fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef tool fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef decision fill:#f3e8ff,stroke:#9333ea,color:#581c87
    classDef model fill:#fce7f3,stroke:#db2777,color:#831843

    class USER,UI,START,ENDNODE user
    class TS,PLAN,EXEC,ANSWER process
    class DATA,CALC,CHART tool
    class ROUTE decision
    class LLM,DATASET model
```

## Workflow Explanation

1. User enters a natural-language question in Streamlit.
2. Tool Selection Node identifies the required tools.
3. Planning Node generates a short execution plan.
4. Conditional Routing decides whether tool execution is required.
5. Tool Execution Node executes the selected Python tools.
6. Answer Generation Node creates an insight using the tool results.
7. Streamlit displays the final answer and visualization.

## Technology Stack

- Python
- LangGraph StateGraph
- LangChain
- Groq LLM
- Pandas
- Plotly
- Streamlit
