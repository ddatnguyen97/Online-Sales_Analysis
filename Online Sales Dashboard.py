import streamlit as st
import pandas as pd

df = pd.read_csv('online_sales_cleaned.csv')

st.title('Online Sales Dashboard')
# st.dataframe(df)
# st.table(df)
# df['TotalSales'] = df['TotalSales'].apply(lambda x: x==0 if x < 0 else x)

st.sidebar.title('Sidebar')
st.bar_chart(df, x='Year', y='TotalSales')
st.bar_chart(df,x='Country', y='TotalSales', color='#36BA98')