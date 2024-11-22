import streamlit as st
import pandas as pd
import plotly.express as px

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

    selected_method = st.selectbox('Payment Method', ['All'] + list(df['PaymentMethod'].unique()))
    if selected_method != 'All':
        filtered_df = df[df['PaymentMethod'] == selected_method]
    else:
        filtered_df = df

total_sales = f"{filtered_df['TotalSales'].sum():,.2f}"       
with st.container():
    col1, col2 = st.columns(2)
    col1.metric('Total Sales', total_sales)
    col2.metric('Quantity', filtered_df['Quantity'].sum())

with st.container():
    if selected_year == 'All':
        st.subheader('Sales by Months')
        sales_by_month = filtered_df.groupby(['Year', 'Month'])['TotalSales'].sum().reset_index()
        sales_by_month_pivot = sales_by_month.pivot(index='Month', columns='Year', values='TotalSales')
        st.line_chart(sales_by_month_pivot)
    else:
        st.subheader('Sales by Month')
        sales_by_month = filtered_df.groupby('Month')['TotalSales'].sum().reset_index()
        st.line_chart(sales_by_month.set_index('Month'))

returned_products_df = filtered_df[filtered_df['ReturnStatus'] == 'Returned']
percentage_of_returned_products = len(returned_products_df) / len(filtered_df) * 100
successful_products_df = filtered_df[filtered_df['ReturnStatus'] != 'Returned']
percentage_of_successful_products = len(successful_products_df) / len(filtered_df) * 100
fig_1 = px.pie(
        names=['Returned', 'Successful'],
        values=[percentage_of_returned_products, 
        percentage_of_successful_products],
        color_discrete_sequence=['#8DECB4','#295F98', ],
        hole=0.5,
        )

payment = filtered_df['PaymentMethod'].value_counts().sort_index()
fig_2 = px.pie(
        names=payment.index,
        values=payment.values,
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.5,
        )
with st.container(): 
    col1, col2 = st.columns(2) 
    with col1: 
        st.subheader('Percentage of Returned Products') 
        st.plotly_chart(fig_1, use_container_width=True) 
    
    with col2: 
        st.subheader('Percentage of Payment Method') 
        st.plotly_chart(fig_2, use_container_width=True)