import pandas as pd

# FULL PATH (use this exactly)
df = pd.read_csv(r"D:\Vs Code\project\superstore.csv", encoding='latin1')

print("First 5 rows:")
print(df.head())

print("\nColumns:")
print(df.columns)

print("\nData Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

# ================== STEP 2 (DATA CLEANING) ==================

# Convert dates to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Extract useful time features
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
df['Month Name'] = df['Order Date'].dt.month_name()

# Check changes
print(df[['Order Date', 'Year', 'Month', 'Month Name']].head())

# ================== STEP 3 (CATEGORY ANALYSIS) ==================

category_summary = df.groupby('Category').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).reset_index()

print("\nCategory Summary:")
print(category_summary)

# ================== STEP 4 (CATEGORY ANALYSIS) ==================

import matplotlib.pyplot as plt
import seaborn as sns

# Bar plot for Sales
plt.figure()
sns.barplot(x='Category', y='Sales', data=category_summary)
plt.title("Sales by Category")
plt.show()

# Bar plot for Profit
plt.figure()
sns.barplot(x='Category', y='Profit', data=category_summary)
plt.title("Profit by Category")
plt.show()

# ================== STEP 5 (SUB-CATEGORY ANALYSIS) ==================

subcat_summary = df.groupby(['Category', 'Sub-Category']).agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).reset_index()

# Sort to find worst performers
subcat_summary = subcat_summary.sort_values(by='Profit')

print("\nSub-Category Summary (Sorted by Profit):")
print(subcat_summary.head(10))

# ================== STEP 6 (LOSS VISUALIZATION) ==================

import matplotlib.pyplot as plt

# Show worst 10 sub-categories
worst = subcat_summary.head(10)

plt.figure()
plt.barh(worst['Sub-Category'], worst['Profit'])
plt.title("Worst Performing Sub-Categories (Profit)")
plt.xlabel("Profit")
plt.ylabel("Sub-Category")
plt.show()

# ================== STEP 7 (REGION ANALYSIS) ==================

region_summary = df.groupby('Region').agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).reset_index()

print("\nRegion Summary:")
print(region_summary)

# ================== STEP 8 (PROFIT MARGIN ANALYSIS) ==================

# Create profit margin
region_summary['Profit Margin'] = (region_summary['Profit'] / region_summary['Sales']) * 100

print("\nRegion Summary with Profit Margin:")
print(region_summary)

# Plot Sales and Profit together
import matplotlib.pyplot as plt

region_summary.set_index('Region')[['Sales', 'Profit']].plot(kind='bar')
plt.title("Sales vs Profit by Region")
plt.ylabel("Amount")
plt.show()

# Plot Profit Margin
plt.figure()
plt.bar(region_summary['Region'], region_summary['Profit Margin'])
plt.title("Profit Margin by Region (%)")
plt.ylabel("Profit Margin (%)")
plt.show()

# ================== STEP 9 (TIME ANALYSIS) ==================

monthly_sales = df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()

print("\nMonthly Sales:")
print(monthly_sales.head())

plt.figure()
plt.plot(monthly_sales['Sales'])
plt.title("Monthly Sales Trend")
plt.xlabel("Time (Month Index)")
plt.ylabel("Sales")
plt.show()

# ================== STEP 10 (CATEGORY TIME TREND) ==================

# Group by Category + Time
monthly_category = df.groupby(['Year', 'Month', 'Category'])['Sales'].sum().reset_index()

# Create proper time index
monthly_category['Date'] = pd.to_datetime(monthly_category[['Year', 'Month']].assign(DAY=1))

# Plot
plt.figure()

for category in monthly_category['Category'].unique():
    subset = monthly_category[monthly_category['Category'] == category]
    plt.plot(subset['Date'], subset['Sales'], label=category)

plt.title("Monthly Sales Trend by Category")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.legend()
plt.show()

# ================== STEP 11 (FORECASTING - TECHNOLOGY) ==================

# Filter Technology data
tech_data = monthly_category[monthly_category['Category'] == 'Technology']

# Sort by date
tech_data = tech_data.sort_values('Date')

# Moving average (window = 3 months)
tech_data['Forecast'] = tech_data['Sales'].rolling(window=3).mean()

# Plot
plt.figure()
plt.plot(tech_data['Date'], tech_data['Sales'], label='Actual')
plt.plot(tech_data['Date'], tech_data['Forecast'], label='Forecast (Moving Avg)')
plt.title("Technology Sales Forecast")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.legend()
plt.show()

# ================== SHIP MODE ANALYSIS ==================

ship_summary = df.groupby('Ship Mode').agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).reset_index()

ship_summary['Profit Margin'] = (ship_summary['Profit'] / ship_summary['Sales']) * 100

print("\nShip Mode Summary:")
print(ship_summary)

# ================== SHIP MODE FIGURES ==================

# fig9 — Sales
fig9, ax9 = plt.subplots(figsize=(8,4))
ax9.bar(ship_summary['Ship Mode'], ship_summary['Sales'])
ax9.set_title("Sales by Ship Mode")


# fig10 — Profit
fig10, ax10 = plt.subplots(figsize=(8,4))
ax10.bar(ship_summary['Ship Mode'], ship_summary['Profit'])
ax10.set_title("Profit by Ship Mode")


# fig11 — Profit Margin
fig11, ax11 = plt.subplots(figsize=(8,4))
ax11.bar(ship_summary['Ship Mode'], ship_summary['Profit Margin'])
ax11.set_title("Profit Margin by Ship Mode")

plt.show()

# ================== STATE ANALYSIS ==================

# Sales by State
state_sales = df.groupby('State')['Sales'].sum().sort_values(ascending=False).head(10)

# Profit by State
state_profit = df.groupby('State')['Profit'].sum().sort_values(ascending=False).head(10)

# Loss-making states
state_loss = df.groupby('State')['Profit'].sum()
state_loss = state_loss[state_loss < 0].sort_values().head(10)

import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
plt.bar(state_sales.index, state_sales.values)
plt.title("Top 10 States by Sales")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10,5))
plt.bar(state_profit.index, state_profit.values)
plt.title("Top 10 States by Profit")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10,5))
plt.bar(state_loss.index, state_loss.values)
plt.title("Top Loss-Making States")
plt.xticks(rotation=45)
plt.show()

print("\nTop 10 States by Sales")
print(state_sales.reset_index())

print("\nTop 10 States by Profit")
print(state_profit.reset_index())

print("\nTop Loss-Making States")
print(state_loss.reset_index())