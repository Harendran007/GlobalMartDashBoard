import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        .main { background-color: #f5f5f5; }
        .stTitle, .stHeader, .stSubheader { color: #333333; }
    </style>
    """,
    unsafe_allow_html=True
)

data = pd.read_csv('superstore.csv', encoding='ISO-8859-1')
data['Order Date'] = pd.to_datetime(data['Order Date'])

total_sales = data['Sales'].sum()
total_profit = data['Profit'].sum()
profit_margin = (total_profit / total_sales) * 100

product_performance = data.groupby("Product Name")[["Sales", "Profit"]].sum().reset_index()
top_sales = product_performance.sort_values(by="Sales", ascending=False).head(10)
top_profit = product_performance.sort_values(by="Profit", ascending=False).head(10)

region_performance = data.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
monthly_region_sales = data.groupby([data['Order Date'].dt.to_period('M'), 'Region'])['Sales'].sum().unstack().fillna(0)
category_sales = data.groupby(["Category", "Sub-Category"])["Sales"].sum().unstack().fillna(0)

st.title("GlobalMart Profitability Dashboard")

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
kpi_col1.metric("Total Sales", f"${total_sales:,.2f}")
kpi_col2.metric("Total Profit", f"${total_profit:,.2f}")
kpi_col3.metric("Profit Margin", f"{profit_margin:.2f}%")

st.subheader("Performance Overview")

grid_col1, grid_col2 = st.columns(2)
with grid_col1:
    fig_sales = px.bar(top_sales, x='Sales', y='Product Name', orientation="h", title="Top 10 Products by Sales", color_discrete_sequence=["#4A90E2"])
    fig_sales.update_layout(xaxis_title="Sales", yaxis_title="", title_font_size=16)
    st.plotly_chart(fig_sales, use_container_width=True)

with grid_col2:
    fig_profit = px.bar(top_profit, x='Profit', y='Product Name', orientation="h", title="Top 10 Products by Profit", color_discrete_sequence=["#50E3C2"])
    fig_profit.update_layout(xaxis_title="Profit", yaxis_title="", title_font_size=16)
    st.plotly_chart(fig_profit, use_container_width=True)

grid_col3, grid_col4 = st.columns(2)
with grid_col3:
    fig_region = px.bar(region_performance, x='Region', y='Sales', title="Sales by Region", color_discrete_sequence=["#F5A623"])
    fig_region.update_layout(xaxis_title="Region", yaxis_title="Sales", title_font_size=16)
    st.plotly_chart(fig_region, use_container_width=True)

with grid_col4:
    fig_monthly_region_sales = go.Figure()
    for region in monthly_region_sales.columns:
        fig_monthly_region_sales.add_trace(go.Scatter(x=monthly_region_sales.index.to_timestamp(), y=monthly_region_sales[region], mode='lines', name=region))
    fig_monthly_region_sales.update_layout(title="Monthly Sales by Region", xaxis_title="Month", yaxis_title="Sales", title_font_size=16)
    st.plotly_chart(fig_monthly_region_sales, use_container_width=True)

grid_col5, grid_col6 = st.columns(2)
with grid_col5:
    fig_category = px.bar(category_sales, barmode='stack', title="Sales by Category and Sub-Category", color_discrete_sequence=px.colors.qualitative.G10)
    fig_category.update_layout(xaxis_title="Category", yaxis_title="Sales", title_font_size=16)
    st.plotly_chart(fig_category, use_container_width=True)

with grid_col6:
    fig_discount = px.scatter(data, x="Discount", y="Profit", opacity=0.6, title="Discount vs Profit", color_continuous_scale="Viridis")
    fig_discount.update_layout(xaxis_title="Discount", yaxis_title="Profit", title_font_size=16)
    st.plotly_chart(fig_discount, use_container_width=True)
