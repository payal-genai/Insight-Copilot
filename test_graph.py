from graph import graph_app

result = graph_app.invoke({
    "question": "What is the average profit?",
    "plan": "",
    "selected_tools": [],
    "tool_results": [],
    "final_answer": ""
})

print("\n--- FINAL ANSWER ---")
print(result["final_answer"])

print("\n--- SELECTED TOOLS ---")
print(result["selected_tools"])

print("\n--- PLAN ---")
print(result["plan"])