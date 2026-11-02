# Design Write-up – Insight Copilot

## 1. Project Overview

Insight Copilot is an AI-powered Sales Data Analyst chatbot built using Python, LangGraph, Groq LLM, Pandas, Plotly and Streamlit. It allows users to ask questions about sales data in natural language and receive meaningful business insights.

## 2. System Architecture

The application uses LangGraph StateGraph to manage the workflow. The workflow consists of tool selection, planning, conditional routing, tool execution and answer generation nodes.

The Streamlit interface accepts user questions and displays the reasoning plan, final answer and charts. Groq LLM (`openai/gpt-oss-120b`) is used for tool selection and answer generation.

## 3. Tool Design

The chatbot uses three tools:

- **Data Query Tool:** Uses Pandas to retrieve total revenue, profit and grouped sales information.
- **Calculator Tool:** Performs calculations such as average and division.
- **Chart Tool:** Generates interactive bar charts using Plotly.

The tool selection node selects the required tools based on the user's question instead of executing every tool for every query.

## 4. Reasoning and Workflow

The chatbot displays a short reasoning plan before executing the selected tools. Conditional routing directs the workflow to tool execution when tools are selected.

The answer generation node uses the tool results and conversation history to generate a clear response with supporting numbers and a business explanation.

Conversation history helps the chatbot understand follow-up questions.

## 5. Data Handling

The project uses the Sales_Dataset_2024.xlsx dataset containing 2,000 records and 10 original columns.

A separate cleaning script handles missing categorical values and creates data quality flags. The cleaned dataset is stored as a CSV file and loaded for analysis. Missing financial values are preserved rather than replaced with zero.

## 6. Limitations and Security

The chatbot answers questions based on the available dataset. It does not assume business reasons that are not supported by the data.

The Groq API key is stored securely using environment variables locally and Streamlit Secrets in the hosted application. Secrets are not committed to GitHub.

## 7. Conclusion

Insight Copilot demonstrates how LangGraph, LLMs and Python tools can work together to build a reasoning-based data analysis chatbot. It provides numerical insights, visualizations and context-aware follow-up responses through a simple web interface.