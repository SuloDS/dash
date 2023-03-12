import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import json

url = "https://www.activityinfo.org/resources/query/v43/form/cgmgor8l0cfilos2"
json_url = requests.get(url)
data = json.loads(json_url.text)

df = pd.DataFrame(data)

st.dataframe(df)


department = df['pv.District.Name'].unique().tolist()


department_selection = st.multiselect('pv.District.Name',
                                    department,
                                    default=department)

# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['pv.District.Name'].isin(department_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['Registado']).count()[['pv.District.Name']]
df_grouped = df_grouped.reset_index()

# --- PLOT BAR CHART
bar_chart = px.bar(df_grouped,
                   x='pv.District.Name',
                   y='Registado',
                   text='Registado',
                   color_discrete_sequence = ['#F63366']*len(df_grouped),
                   template= 'plotly_white')
st.plotly_chart(bar_chart)