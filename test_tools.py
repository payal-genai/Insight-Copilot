
from tools import (
    data_query_tool,
    calculator_tool,
    chart_tool
)

print("\n--- TOTAL SUMMARY ---")
print(data_query_tool())

print("\n--- REGION-WISE REVENUE ---")
print(data_query_tool(
    query_type="group",
    group_by="Region",
    metric="Revenue"
))

print("\n--- PRODUCT-WISE PROFIT ---")
print(data_query_tool(
    query_type="group",
    group_by="Product",
    metric="Profit"
))

print("\n--- CALCULATOR ---")
print("Average:", calculator_tool("average", [100, 200, 300]))

print("\n--- CHART ---")
chart = chart_tool("Region", "Revenue")
print("Chart created:", type(chart))
