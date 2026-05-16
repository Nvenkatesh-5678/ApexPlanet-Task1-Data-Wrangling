import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =========================================================
# CREATE REQUIRED FOLDERS AUTOMATICALLY
# =========================================================

os.makedirs("../cleaned_data", exist_ok=True)
os.makedirs("../visualizations", exist_ok=True)

# =========================================================
# LOAD DATASET
# =========================================================

df = pd.read_csv("../dataset/Sample - Superstore.csv", encoding="latin1")

print("=" * 60)
print("FIRST 5 ROWS")
print("=" * 60)
print(df.head())

# =========================================================
# DATASET INFORMATION
# =========================================================

print("\n" + "=" * 60)
print("DATASET INFO")
print("=" * 60)
print(df.info())

# =========================================================
# STATISTICAL SUMMARY
# =========================================================

print("\n" + "=" * 60)
print("STATISTICAL SUMMARY")
print("=" * 60)
print(df.describe())

# =========================================================
# MISSING VALUES
# =========================================================

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)
print(df.isnull().sum())

# =========================================================
# DUPLICATE ROWS
# =========================================================

print("\n" + "=" * 60)
print("DUPLICATE ROWS")
print("=" * 60)
print(df.duplicated().sum())

# Remove duplicate rows
df = df.drop_duplicates()

# =========================================================
# DATA CLEANING
# =========================================================

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Convert date columns
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# =========================================================
# FEATURE ENGINEERING
# =========================================================

# Extract Order Year
df['Order Year'] = df['Order Date'].dt.year

# Extract Order Month
df['Order Month'] = df['Order Date'].dt.month

# Create Profit Percentage column
df['Profit Percentage'] = (df['Profit'] / df['Sales']) * 100

# =========================================================
# OUTLIER DETECTION USING IQR METHOD
# =========================================================

Q1 = df['Sales'].quantile(0.25)
Q3 = df['Sales'].quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - (1.5 * IQR)
upper_bound = Q3 + (1.5 * IQR)

outliers = df[
    (df['Sales'] < lower_bound) |
    (df['Sales'] > upper_bound)
]

print("\n" + "=" * 60)
print("NUMBER OF OUTLIERS IN SALES COLUMN")
print("=" * 60)
print(outliers.shape[0])

# =========================================================
# SAVE CLEANED DATASET
# =========================================================

df.to_csv("../cleaned_data/cleaned_superstore.csv", index=False)

print("\nCLEANED DATASET SAVED SUCCESSFULLY")

# =========================================================
# DATA VISUALIZATIONS
# =========================================================

sns.set()

# ---------------------------------------------------------
# 1. SALES DISTRIBUTION
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))
sns.histplot(df['Sales'], bins=30)

plt.title("Sales Distribution")
plt.xlabel("Sales")
plt.ylabel("Frequency")

plt.savefig("../visualizations/sales_distribution.png")
plt.close()

# ---------------------------------------------------------
# 2. PROFIT DISTRIBUTION
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))
sns.histplot(df['Profit'], bins=30)

plt.title("Profit Distribution")
plt.xlabel("Profit")
plt.ylabel("Frequency")

plt.savefig("../visualizations/profit_distribution.png")
plt.close()

# ---------------------------------------------------------
# 3. ORDERS BY REGION
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.barplot(
    x=df['Region'].value_counts().index,
    y=df['Region'].value_counts().values
)

plt.title("Orders by Region")
plt.xlabel("Region")
plt.ylabel("Number of Orders")

plt.savefig("../visualizations/orders_by_region.png")
plt.close()

# ---------------------------------------------------------
# 4. SALES BY CATEGORY
# ---------------------------------------------------------

category_sales = df.groupby('Category')['Sales'].sum()

plt.figure(figsize=(8, 5))

category_sales.plot(kind='bar')

plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")

plt.savefig("../visualizations/sales_by_category.png")
plt.close()

# ---------------------------------------------------------
# 5. CORRELATION HEATMAP
# ---------------------------------------------------------

numeric_df = df.select_dtypes(include=['int64', 'float64'])

plt.figure(figsize=(10, 6))

sns.heatmap(
    numeric_df.corr(),
    annot=True
)

plt.title("Correlation Heatmap")

plt.savefig("../visualizations/correlation_heatmap.png")
plt.close()

print("\nVISUALIZATIONS GENERATED SUCCESSFULLY")

# =========================================================
# CREATE DATA DICTIONARY
# =========================================================

descriptions = [
    'Unique row identifier',
    'Unique order identifier',
    'Order purchase date',
    'Shipping date',
    'Shipping method',
    'Unique customer identifier',
    'Customer full name',
    'Customer segment',
    'Country name',
    'City name',
    'State name',
    'Postal code',
    'Sales region',
    'Unique product identifier',
    'Product category',
    'Product sub-category',
    'Product name',
    'Sales amount',
    'Quantity sold',
    'Discount applied',
    'Profit earned',
    'Order year',
    'Order month',
    'Profit percentage'
]

# Ensure descriptions length matches columns
while len(descriptions) < len(df.columns):
    descriptions.append("Column description")

data_dict = pd.DataFrame({
    'Column Name': df.columns,
    'Data Type': df.dtypes.astype(str),
    'Non-Null Count': df.count().values,
    'Description': descriptions[:len(df.columns)]
})

# Save Data Dictionary
data_dict.to_excel("../data_dictionary.xlsx", index=False)

print("\nDATA DICTIONARY CREATED SUCCESSFULLY")

# =========================================================
# FINAL MESSAGE
# =========================================================

print("\n" + "=" * 60)
print("TASK 1 DATA WRANGLING COMPLETED SUCCESSFULLY")
print("=" * 60)

print("""
Generated Files:
1. Cleaned Dataset
2. Data Dictionary
3. Data Visualizations
4. Feature Engineered Dataset
5. Outlier Detection Report
""")