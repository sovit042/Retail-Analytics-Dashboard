import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ================== LOAD DATA ==================
df = pd.read_csv("superstore.csv", encoding='latin-1')

# Convert date
df['Order Date'] = pd.to_datetime(df['Order Date'])

# ================== SIDEBAR FILTER ==================
st.sidebar.header("Filters")

categories = st.sidebar.multiselect(
    "Select Category",
    df['Category'].unique(),
    default=df['Category'].unique()
)

filtered_df = df[df['Category'].isin(categories)]

# Category Summary
category_summary = filtered_df.groupby('Category')[['Sales', 'Profit']].sum().reset_index()

# Sub-Category Summary
subcat_summary = filtered_df.groupby('Sub-Category')[['Sales', 'Profit']].sum().reset_index()
subcat_summary = subcat_summary.sort_values(by='Profit')

# Region Summary
region_summary = filtered_df.groupby('Region')[['Sales', 'Profit']].sum().reset_index()
region_summary['Profit Margin'] = (region_summary['Profit'] / region_summary['Sales']) * 100

# Monthly Sales
filtered_df['Month-Year'] = filtered_df['Order Date'].dt.to_period('M').astype(str)
monthly_sales = filtered_df.groupby('Month-Year')['Sales'].sum().reset_index()
monthly_sales['Date'] = pd.to_datetime(monthly_sales['Month-Year'])
monthly_sales = monthly_sales.sort_values('Date')

# Category Trend
category_trend = filtered_df.groupby(['Month-Year', 'Category'])['Sales'].sum().unstack()
category_trend.index = pd.to_datetime(category_trend.index)
category_trend = category_trend.sort_index()

# ================== FORECAST ==================

tech_df = filtered_df[filtered_df['Category'] == 'Technology'].copy()

# 🔥 Force datetime conversion
tech_df['Order Date'] = pd.to_datetime(tech_df['Order Date'], errors='coerce')

# 🔥 Drop bad rows (important)
tech_df = tech_df.dropna(subset=['Order Date'])

# 🔥 Set index FIRST (this is what you were missing)
tech_df = tech_df.set_index('Order Date')

# 🔥 Now group + resample works
tech_sales = tech_df['Sales'].resample('MS').sum()

# Forecast
from statsmodels.tsa.arima.model import ARIMA

# ================== FORECAST (REAL MODEL) ==================

# Fit ARIMA model
model = ARIMA(tech_sales, order=(2,1,2))
model_fit = model.fit()

# Forecast next 6 months
forecast_steps = 6
forecast = model_fit.forecast(steps=forecast_steps)

# Create future dates
future_dates = pd.date_range(start=tech_sales.index[-1], periods=forecast_steps+1, freq='MS')[1:]

tech_forecast = pd.Series(forecast.values, index=future_dates)

# Sales by Category
fig1, ax1 = plt.subplots()
ax1.bar(category_summary['Category'], category_summary['Sales'])
ax1.set_title("Sales by Category")

# Profit by Category
fig2, ax2 = plt.subplots()
ax2.bar(category_summary['Category'], category_summary['Profit'])
ax2.set_title("Profit by Category")

# Worst Sub-Category
fig3, ax3 = plt.subplots()
ax3.barh(subcat_summary['Sub-Category'], subcat_summary['Profit'])
ax3.set_title("Worst Sub-Categories")

# Region Sales vs Profit
fig4, ax4 = plt.subplots()
x = region_summary['Region']
ax4.bar(x, region_summary['Sales'], label='Sales')
ax4.bar(x, region_summary['Profit'], label='Profit')
ax4.legend()
ax4.set_title("Sales vs Profit by Region")

# Profit Margin
fig5, ax5 = plt.subplots()
ax5.bar(region_summary['Region'], region_summary['Profit Margin'])
ax5.set_title("Profit Margin by Region")

# Monthly Trend
fig6, ax6 = plt.subplots(figsize=(10,5))

ax6.plot(monthly_sales['Date'], monthly_sales['Sales'])

ax6.set_title("Monthly Sales Trend")

# 🔥 Clean x-axis
import matplotlib.dates as mdates
ax6.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax6.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax6.xaxis.set_minor_locator(mdates.MonthLocator())

ax6.grid(which='major', linestyle='--', alpha=0.6)
ax6.grid(which='minor', linestyle=':', alpha=0.3)

plt.xticks(rotation=45)

# Category Trend
fig7, ax7 = plt.subplots(figsize=(10,5))

for col in category_trend.columns:
    ax7.plot(category_trend.index, category_trend[col], label=col)

ax7.legend()
ax7.set_title("Sales Trend by Category")

#Forecast
fig8, ax8 = plt.subplots(figsize=(10,5))

# Actual data
ax8.plot(tech_sales.index, tech_sales, label='Actual', color='blue')

# 🔥 Fix bad starting drop
tech_forecast.iloc[0] = tech_sales.iloc[-1]

# 🔥 Combine for smooth transition
combined_index = tech_sales.index.append(tech_forecast.index)
combined_values = list(tech_sales.values) + list(tech_forecast.values)

ax8.plot(combined_index, combined_values, linestyle='--', color='red', label='Forecast')

# 🔥 Confidence band
ax8.fill_between(
    tech_forecast.index,
    tech_forecast * 0.9,
    tech_forecast * 1.1,
    color='red',
    alpha=0.2
)

ax8.set_title("Technology Sales Forecast (ARIMA)")
ax8.legend()

# Convert to DataFrame
actual_df = tech_sales.reset_index()
actual_df.columns = ['Date', 'Actual Sales']
actual_df['Forecast'] = None

forecast_df = tech_forecast.reset_index()
forecast_df.columns = ['Date', 'Forecast']
forecast_df['Actual Sales'] = None

# Combine
final_df = pd.concat([actual_df, forecast_df], ignore_index=True)

# Sort by date
final_df = final_df.sort_values('Date')

import matplotlib.dates as mdates
# Major ticks (big labels)
ax7.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax7.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Minor ticks (small lines every month)
ax7.xaxis.set_minor_locator(mdates.MonthLocator())

ax7.grid(which='major', linestyle='--', alpha=0.6)
ax7.grid(which='minor', linestyle=':', alpha=0.3)

# Rotate labels
plt.xticks(rotation=45)

st.title("Retail Business Dashboard")

# Category
st.header("Category Performance")
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig1)
with col2:
    st.pyplot(fig2)

best_cat = category_summary.sort_values(by='Profit', ascending=False).iloc[0]

st.subheader("🏆 Best Performing Category")

st.success(f"{best_cat['Category']} is generating highest profit: {best_cat['Profit']:.2f}")

with st.expander("📊 View Category Data"):
    st.dataframe(category_summary)

with st.expander("📊 View Profit Data"):
    st.dataframe(category_summary[['Category', 'Profit']])

# Risk
st.header("Risk Analysis")
st.pyplot(fig3)

worst = subcat_summary.iloc[0]
st.warning(f"{worst['Sub-Category']} is making lowest profit: {worst['Profit']:.2f}")

st.subheader("📌 Recommended Action")

st.info(f"""
Focus on **{worst['Sub-Category']}**:
- Reduce heavy discounts
- Optimize pricing strategy
- If losses continue, consider removing or replacing this product line
""")

with st.expander("📊 View Sub-Category Data"):
    st.dataframe(subcat_summary)

# Region
st.header("Regional Insights")
st.pyplot(fig4)
st.pyplot(fig5)

worst_region = region_summary.sort_values(by='Profit').iloc[0]

st.subheader("⚠️ Weakest Region")

st.error(f"{worst_region['Region']} has lowest profit: {worst_region['Profit']:.2f}")

with st.expander("📊 View Region Data"):
    st.dataframe(region_summary)

with st.expander("📊 View Profit Margin Data"):
    st.dataframe(region_summary[['Region', 'Profit Margin']])

# Trends
st.header("Trends")
st.pyplot(fig6)
st.pyplot(fig7)

st.subheader("🧠 Business Recommendation")

if worst_region['Profit'] < 0:
    st.warning("Focus on improving performance in this region. Consider reducing discounts or optimizing logistics.")
else:
    st.info("All regions are profitable. Focus on scaling high-performing regions.")

with st.expander("📊 View Monthly Sales Data"):
    st.dataframe(monthly_sales)

with st.expander("📊 View Category Trend Data"):
    st.dataframe(category_trend)

#Technology Sales Forecast
st.header("📈 Forecast")

st.pyplot(fig8)

with st.expander("📊 View Forecast Data"):
    st.dataframe(final_df)