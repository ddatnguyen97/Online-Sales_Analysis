import streamlit as st
from streamlit_dynamic_filters import DynamicFilters
import pandas as pd
import plotly.express as px

df = pd.read_csv('online_sales_cleaned.csv')

st.title('Online Sales Dashboard')

# list_years = ['All'] + sorted(list(df['Year'].unique()))
# list_channels = ['All'] + sorted(list(df['SalesChannel'].unique()))
# list_payments = ['All'] + sorted(list(df['PaymentMethod'].unique()))
# list_country = ['All'] + sorted(list(df['Country'].unique()))

# with st.sidebar:
#     st.title('Menu')
#     selected_year = st.selectbox('Year', list_years)
#     selected_method = st.selectbox('Payment Method', list_channels)
#     selected_channel = st.selectbox('Sales Channel', list_payments)
#     selected_country = st.selectbox('Country', list_country)

# filtered_df = df
# if selected_year != 'All':
#     filtered_df = filtered_df[filtered_df['Year'] == selected_year]
# if selected_method != 'All':
#     filtered_df = filtered_df[filtered_df['PaymentMethod'] == selected_method]
# if selected_channel != 'All':
#     filtered_df = filtered_df[filtered_df['SalesChannel'] == selected_channel]
# if selected_country != 'All':
#     filtered_df = filtered_df[filtered_df['Country'] == selected_country]

dynamic_filters = DynamicFilters(df, filters=['Year', 'SalesChannel', 'PaymentMethod' , 'Country', 'Category'])
with st.sidebar:
    st.title('Filters')
    dynamic_filters.display_filters()

filtered_df = dynamic_filters.filter_df()

def format_number(number):
    if number >= 1000000000:
        return f'{number/1000000000:.1f}B'
    elif number >= 1000000:
        return f'{number/1000000:.1f}M'
    elif number >= 1000:
        return f'{number/1000:.1f}K'
    else:
        return number

total_sales = filtered_df['TotalSales'].sum()
formatted_total_sales = format_number(total_sales)
total_quantity = filtered_df['Quantity'].sum()
formatted_total_quantity = format_number(total_quantity)

returned_products_df = filtered_df[filtered_df['ReturnStatus'] == 'Returned']
percentage_of_returned_products = len(returned_products_df) / len(filtered_df) * 100
successful_products_df = filtered_df[filtered_df['ReturnStatus'] != 'Returned']
percentage_of_successful_products = len(successful_products_df) / len(filtered_df) * 100

with st.container():
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Total Sales', formatted_total_sales)
    col2.metric('Quantity', formatted_total_quantity)
    col3.metric('Returned Products', f"{percentage_of_returned_products:.2f}%")
    col4.metric('Successful Products', f"{percentage_of_successful_products:.2f}%")

with st.container():
    st.subheader('Sales by Months')
    sales_by_month = filtered_df.groupby(['Year', 'Month'])['TotalSales'].sum().reset_index()
    sales_by_month_pivot = sales_by_month.pivot(index='Month', columns='Year', values='TotalSales')
    st.line_chart(sales_by_month_pivot)

channels = filtered_df['SalesChannel'].value_counts().sort_index()
fig_1 = px.pie(
        names=channels.index,
        values=channels.values,
        color_discrete_sequence=['#8DECB4','#295F98',],
        hole=0.5,
        )

payments = filtered_df['PaymentMethod'].value_counts().sort_index()
fig_2 = px.pie(
        names=payments.index,
        values=payments.values,
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.5,
        )
with st.container(): 
    col1, col2 = st.columns(2) 
    with col1: 
        st.subheader('Percentages of Sales Channel') 
        st.plotly_chart(fig_1, use_container_width=True) 
    
    with col2: 
        st.subheader('Percentages of Payment Method') 
        st.plotly_chart(fig_2, use_container_width=True)

countries = filtered_df['Country'].value_counts().sort_index()
fig_3 = px.bar(
        x=countries.values,
        y=countries.index,
        labels={'x':'Counts', 'y':'Country'},
        color=countries.index,
        color_discrete_sequence=px.colors.qualitative.Set2,
        orientation='h',
        )
fig_3.update_layout(showlegend=False)

categories = filtered_df['Category'].value_counts().sort_index()
fig_4 = px.pie(
        names=categories.index,
        values=categories.values,
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.5,
        )

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Sales by Country')
        st.plotly_chart(fig_3, use_container_width=True)

    with col2:
        st.subheader('Sales by Category')
        st.plotly_chart(fig_4, use_container_width=True)
        