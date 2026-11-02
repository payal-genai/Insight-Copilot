
import pandas as pd
import plotly.express as px

DATA_PATH = "data/cleaned_sales_data.csv"


def load_data():
    """Load cleaned sales dataset."""
    return pd.read_csv(DATA_PATH)


# TOOL 1: DATA QUERY TOOL
def data_query_tool(
    query_type="summary",
    group_by=None,
    metric="Revenue",
    column=None,
    value=None
):

    df = load_data()

    if query_type == "summary":

        return {
    "total_records": int(len(df)),
    "total_revenue": float(round(df["Revenue"].sum(), 2)),
    "total_profit": float(round(df["Profit"].sum(), 2)),
    "average_profit": float(round(df["Profit"].mean(), 2)),
    "valid_revenue_records": int(df["Revenue"].count()),
    "valid_profit_records": int(df["Profit"].count())
}

    elif query_type == "group":

        if group_by not in df.columns:
            return "Invalid group column"

        if metric not in ["Revenue", "Profit", "Units_Sold"]:
            return "Invalid metric"

        result = (
            df.groupby(group_by)[metric]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        return result.to_dict(orient="records")

    elif query_type == "filter":

        if column not in df.columns:
            return "Invalid column name"

        filtered_df = df[df[column] == value]

        return filtered_df.head(20).to_dict(orient="records")

    return "Invalid query type"


# TOOL 2: CALCULATOR TOOL
def calculator_tool(operation, numbers):

    if not numbers:
        return "No numbers provided"

    if operation == "sum":
        return sum(numbers)

    elif operation == "average":
        return sum(numbers) / len(numbers)

    elif operation == "divide":
        if len(numbers) != 2 or numbers[1] == 0:
            return "Division requires two numbers and a non-zero denominator"

        return numbers[0] / numbers[1]

    elif operation == "percentage":

        if len(numbers) != 2 or numbers[1] == 0:
            return "Percentage requires two numbers and a non-zero denominator"

        return (numbers[0] / numbers[1]) * 100

    return "Invalid operation"


# TOOL 3: CHART TOOL
def chart_tool(group_by="Region", metric="Revenue"):

    df = load_data()

    if group_by not in df.columns:
        return "Invalid group column"

    if metric not in ["Revenue", "Profit", "Units_Sold"]:
        return "Invalid metric"

    chart_data = (
        df.groupby(group_by)[metric]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        chart_data,
        x=group_by,
        y=metric,
        title=f"{metric} by {group_by}"
    )

    return fig
