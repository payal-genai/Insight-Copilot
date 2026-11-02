import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/cleaned_sales_data.csv")

print("--- CLEANED DATASET ---")
print(df.head())

print("\n--- DATASET SHAPE ---")
print(df.shape)

print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

print("\n--- DATA QUALITY SUMMARY ---")

print("Total Records:", len(df))

print(
    "Negative Unit Price:",
    df["is_negative_unit_price"].sum()
)

print(
    "Negative Units Sold:",
    df["is_negative_units_sold"].sum()
)

print(
    "Incomplete Financial Records:",
    df["has_missing_financial_data"].sum()
)