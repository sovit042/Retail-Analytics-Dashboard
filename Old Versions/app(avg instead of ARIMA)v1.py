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
tech_forecast = tech_sales.rolling(window=3).mean()

#shipmode
ship_modes = st.sidebar.multiselect(
    "Select Ship Mode",
    df['Ship Mode'].unique(),
    default=df['Ship Mode'].unique()
)

filtered_df = df[
    (df['Category'].isin(categories)) &
    (df['Ship Mode'].isin(ship_modes))
]

ship_summary = filtered_df.groupby('Ship Mode').agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).reset_index()

ship_summary['Profit Margin'] = (ship_summary['Profit'] / ship_summary['Sales']) * 100

#STATE ANALYSIS

state_summary = filtered_df.groupby('State').agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).reset_index()

# Sort for better visualization
top_states_sales = state_summary.sort_values(by='Sales', ascending=False).head(10)
top_states_profit = state_summary.sort_values(by='Profit', ascending=False).head(10)
loss_states = state_summary.sort_values(by='Profit').head(10)

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
fig4, ax4 = plt.subplots(figsize=(10,5))
x = region_summary['Region']
ax4.bar(x, region_summary['Sales'], label='Sales')
ax4.bar(x, region_summary['Profit'], label='Profit')
ax4.legend()
ax4.set_title("Sales vs Profit by Region")
fig4.tight_layout()

# Profit Margin
fig5, ax5 = plt.subplots(figsize=(10,5))
ax5.bar(region_summary['Region'], region_summary['Profit Margin'])
ax5.set_title("Profit Margin by Region")
fig5.tight_layout()

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

#Forecast
fig8, ax8 = plt.subplots(figsize=(10,5))

ax8.plot(tech_sales.index, tech_sales, label='Actual')
ax8.plot(tech_forecast.index, tech_forecast, label='Forecast')

ax8.set_title("Technology Sales Forecast")
ax8.legend()

# Major ticks (big labels)
ax8.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax8.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Minor ticks (small lines every month)
ax8.xaxis.set_minor_locator(mdates.MonthLocator())

ax8.grid(which='major', linestyle='--', alpha=0.6)
ax8.grid(which='minor', linestyle=':', alpha=0.3)

# Rotate labels
plt.xticks(rotation=45)

import matplotlib.dates as mdates

#SHIP MODE FIGURES

# fig9 — Sales
fig9, ax9 = plt.subplots(figsize=(8,4))
ax9.bar(ship_summary['Ship Mode'], ship_summary['Sales'])
ax9.set_title("Sales by Ship Mode")

# fig10 — Profit
fig10, ax10 = plt.subplots(figsize=(8,4))
ax10.bar(ship_summary['Ship Mode'], ship_summary['Profit'])
ax10.set_title("Profit by Ship Mode")
fig10.tight_layout()

# fig11 — Profit Margin
fig11, ax11 = plt.subplots(figsize=(8,4))
ax11.bar(ship_summary['Ship Mode'], ship_summary['Profit Margin'])
ax11.set_title("Profit Margin by Ship Mode")
fig11.tight_layout()

fig12, ax12 = plt.subplots(figsize=(10,5))
ax12.bar(top_states_sales['State'], top_states_sales['Sales'])
ax12.set_title("Top 10 States by Sales")
plt.xticks(rotation=45)

fig13, ax13 = plt.subplots(figsize=(10,5))
ax13.bar(top_states_profit['State'], top_states_profit['Profit'])
ax13.set_title("Top 10 States by Profit")
plt.xticks(rotation=45)

fig14, ax14 = plt.subplots(figsize=(10,5))
ax14.bar(loss_states['State'], loss_states['Profit'], color='red')  # already negative
ax14.set_title("Top Loss-Making States")
ax14.set_ylabel("Loss Amount")
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
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig4)
with col2:
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
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig6)
with col2:
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
    forecast_df = pd.DataFrame({
        'Date': tech_sales.index,
        'Actual Sales': tech_sales.values,
        'Forecast': tech_forecast.values
    })
    st.dataframe(forecast_df)

st.header("🚚 Ship Mode Analysis")
st.pyplot(fig9)

col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig10)
with col2:
    st.pyplot(fig11)

best_ship = ship_summary.sort_values(by='Profit', ascending=False).iloc[0]
st.success(f"{best_ship['Ship Mode']} is generating highest profit: {best_ship['Profit']:.2f}")

with st.expander("📊 View Ship Mode Data"):
    st.dataframe(ship_summary)

#State Analysis
st.header("🏙️ State Analysis")
st.pyplot(fig12)
col1, col2, = st.columns(2)

with col1:
    st.pyplot(fig13)

with col2:
    st.pyplot(fig14)

worst_state = state_summary.sort_values(by='Profit').iloc[0]
best_state = state_summary.sort_values(by='Profit', ascending=False).iloc[0]
col1, col2 = st.columns(2)
with col1:
    st.success(f"""
📈 **Highest Profit**
**State:** {best_state['State']}  
**Amount:** {best_state['Profit']:.2f}
""")    
with col2:
    st.error(f"""
📉 **Highest Loss**
**State:** {worst_state['State']}  
**Amount:** {worst_state['Profit']:.2f}
""")

with st.expander("📊 State Data Table"):
    st.dataframe(state_summary)