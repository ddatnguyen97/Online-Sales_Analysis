import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('online_sales_cleaned.csv')

st.title('Online Sales Dashboard')

years = ['All'] + list(df['Year'].unique())
with st.sidebar:
    st.title('Sidebar')
    selected_year = st.selectbox('Year', years)
    if selected_year == 'All':
        filtered_df = df
    else:
        filtered_df = df[df['Year'] == selected_year]

total_sales = f"{filtered_df['TotalSales'].sum():,.2f}"       
with st.container():
    col1, col2 = st.columns(2)
    col1.metric('Total Sales', total_sales)
    col2.metric('Quantity', filtered_df['Quantity'].sum())
    # st.metric('Total Sales', filtered_df['TotalSales'].sum())
    # st.metric('Quantity', filtered_df['Quantity'].sum())

# with st.container():
#     st.map(filtered_df.groupby('Country').size())

with st.container():
    if selected_year == 'All':
        sales_by_month = filtered_df.groupby(['Year', 'Month'])['TotalSales'].sum().reset_index()
        sales_by_month_pivot = sales_by_month.pivot(index='Month', columns='Year', values='TotalSales')
        st.line_chart(sales_by_month_pivot)
    else:
        sales_by_month = filtered_df.groupby('Month')['TotalSales'].sum().reset_index()
        st.line_chart(sales_by_month.set_index('Month'))