import pandas as pd

# Load dataset
df = pd.read_excel("data/Sales_Dataset_2024.xlsx")

# 1. Display first 5 rows
print("\n--- FIRST 5 ROWS ---")
print(df.head())

# 2. Check number of rows and columns
print("\n--- DATASET SHAPE ---")
print(df.shape)

# 3. Display all column names
print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

# 4. Check data types
print("\n--- DATA TYPES ---")
print(df.dtypes)

# 5. Check missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

# 6. Statistical summary
print("\n--- STATISTICAL SUMMARY ---")
print(df.describe())



# 7. Check duplicate records
print("\n--- DUPLICATE RECORDS ---")
print(df.duplicated().sum())

# 8. Check negative values
print("\n--- NEGATIVE VALUES ---")
print("Negative Units:", (df["Units_Sold"] < 0).sum())
print("Negative Revenue:", (df["Revenue"] < 0).sum())
print("Negative Cost:", (df["Cost"] < 0).sum())
print("Negative Profit:", (df["Profit"] < 0).sum())

# 9. Display rows with missing Revenue
print("\n--- MISSING REVENUE ROWS ---")
print(df[df["Revenue"].isnull()].head(10))

# 10. Display negative Units records
print("\n--- NEGATIVE UNITS RECORDS ---")
print(df[df["Units_Sold"] < 0].head(10))


# 11. Check missing values row by row
print("\n--- MISSING VALUE DETAILS ---")

missing_rows = df[df.isnull().any(axis=1)]

print(missing_rows.head(15).to_string())

# 12. Check negative records completely
print("\n--- ALL NEGATIVE RECORDS ---")

negative_rows = df[
    (df["Units_Sold"] < 0) |
    (df["Revenue"] < 0) |
    (df["Cost"] < 0) |
    (df["Profit"] < 0)
]

print(negative_rows.to_string())

# 13. Check relationship between Revenue, Cost and Profit
print("\n--- PROFIT VALIDATION ---")

valid_rows = df.dropna(subset=["Revenue", "Cost", "Profit"])

print(
    "Incorrect Profit Calculations:",
    (abs(valid_rows["Revenue"] - valid_rows["Cost"]
         - valid_rows["Profit"]) > 0.01).sum()
)

# 14. Validate Revenue calculation

print("\n--- REVENUE VALIDATION ---")

valid_revenue_rows = df.dropna(
    subset=["Units_Sold", "Unit_Price", "Revenue"]
)

calculated_revenue = (
    valid_revenue_rows["Units_Sold"] *
    valid_revenue_rows["Unit_Price"]
)

incorrect_revenue = (
    abs(valid_revenue_rows["Revenue"] - calculated_revenue) > 0.01
)

print("Valid Revenue Rows:", len(valid_revenue_rows))

print(
    "Incorrect Revenue Calculations:",
    incorrect_revenue.sum()
)

print("\n--- INCORRECT REVENUE RECORDS ---")

print(
    valid_revenue_rows[incorrect_revenue].to_string()
)

# 15. Dataset structure verification

print("\n--- DATASET SHEET DETAILS ---")

excel_file = pd.ExcelFile("data/Sales_Dataset_2024.xlsx")

for sheet in excel_file.sheet_names:
    print("Sheet Name:", sheet)

print("\n--- ALL COLUMN NAMES ---")
print(df.columns.tolist())

print("\n--- RANDOM 10 RECORDS ---")
print(df.sample(10).to_string(index=False))


# STEP 13: Data quality summary

print("\n--- DATA QUALITY SUMMARY ---")

print("Total Rows:", len(df))

print(
    "Rows with missing values:",
    df.isnull().any(axis=1).sum()
)

print(
    "Rows with negative Unit Price:",
    (df["Unit_Price"] < 0).sum()
)

print(
    "Rows with negative Units Sold:",
    (df["Units_Sold"] < 0).sum()
)

print(
    "Rows with complete financial data:",
    df.dropna(
        subset=["Units_Sold", "Unit_Price", "Revenue", "Cost", "Profit"]
    ).shape[0]
)