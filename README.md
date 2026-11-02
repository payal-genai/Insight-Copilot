# Insight Copilot

An AI-powered Sales Data Analyst chatbot built using
LangGraph, Python, Pandas, Groq LLM and Streamlit.

## Project Overview

Insight Copilot allows users to ask natural-language
questions about sales data and receive meaningful insights.

It can:
- Calculate total revenue and profit.
- Calculate average revenue and profit.
- Compare revenue across regions.
- Generate bar charts using Plotly.
- Handle follow-up questions using conversation history.
- Provide a reasoning plan before executing tools.

## Tech Stack

- Python
- LangGraph
- LangChain
- Groq LLM
- Pandas
- Plotly
- Streamlit

## Tools

1. Data Query Tool
2. Calculator Tool
3. Chart Tool

## Dataset

Sales_Dataset_2024.xlsx

- 2,000 records
- 10 original columns

## Run Locally

1. Clone the repository.
2. Create a virtual environment.
3. Install dependencies:

   pip install -r requirements.txt

4. Add your Groq API key to `.env`:

   GROQ_API_KEY=your_api_key

5. Run the application:

   streamlit run app.py

## Security

API keys are stored in environment variables
and are not committed to GitHub.