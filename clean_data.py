import pandas as pd

# 1. Load original dataset
df = pd.read_excel("data/Sales_Dataset_2024.xlsx")

# 2. Create a copy
clean_df = df.copy()

# 3. Handle missing text values
text_columns = [
    "Region",
    "Product",
    "Salesperson"
]

for col in text_columns:
    clean_df[col] = clean_df[col].fillna("Unknown")

# 4. Add data quality flags
clean_df["is_negative_unit_price"] = (
    clean_df["Unit_Price"] < 0
)

clean_df["is_negative_units_sold"] = (
    clean_df["Units_Sold"] < 0
)

clean_df["has_missing_financial_data"] = (
    clean_df[
        ["Units_Sold", "Unit_Price", "Revenue", "Cost", "Profit"]
    ].isnull().any(axis=1)
)

# 5. Save cleaned dataset
clean_df.to_csv(
    "data/cleaned_sales_data.csv",
    index=False
)

# 6. Display results
print("Cleaned dataset created successfully!")

print("Original rows:", len(df))
print("Cleaned rows:", len(clean_df))

print("\nRemaining missing values:")
print(clean_df.isnull().sum())

print("\nData quality flags:")
print(
    clean_df[
        [
            "is_negative_unit_price",
            "is_negative_units_sold",
            "has_missing_financial_data"
        ]
    ].sum()
)