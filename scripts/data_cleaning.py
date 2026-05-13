import pandas as pd

# Load dataset
df = pd.read_csv("../dataset/Sample - Superstore.csv", encoding="latin1")

# Display first rows
print("FIRST 5 ROWS")
print(df.head())

# Dataset information
print("\nDATASET INFO")
print(df.info())

# Statistical summary
print("\nSTATISTICAL SUMMARY")
print(df.describe())

# Check missing values
print("\nMISSING VALUES")
print(df.isnull().sum())

# Check duplicate rows
print("\nDUPLICATE ROWS")
print(df.duplicated().sum())

# Remove duplicates
df = df.drop_duplicates()

# Convert date columns
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Feature Engineering
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month

# Create Profit Percentage column
df['Profit Percentage'] = (df['Profit'] / df['Sales']) * 100

# Remove extra spaces from columns
df.columns = df.columns.str.strip()

# Save cleaned dataset
df.to_csv("../cleaned_data/cleaned_superstore.csv", index=False)

# Detect Outliers using IQR

Q1 = df['Sales'].quantile(0.25)
Q3 = df['Sales'].quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df['Sales'] < lower_bound) | (df['Sales'] > upper_bound)]

print("\nNUMBER OF OUTLIERS IN SALES COLUMN:")
print(outliers.shape[0])

print("\nDATA CLEANING COMPLETED")
print("Cleaned dataset saved successfully.")

# Create Data Dictionary Automatically

data_dict = pd.DataFrame({
    'Column Name': df.columns,
    'Data Type': df.dtypes.astype(str),
    'Non-Null Count': df.count().values,
    'Description': [
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
})

# Save Data Dictionary
data_dict.to_excel("../data_dictionary.xlsx", index=False)

print("\nDATA DICTIONARY CREATED SUCCESSFULLY")