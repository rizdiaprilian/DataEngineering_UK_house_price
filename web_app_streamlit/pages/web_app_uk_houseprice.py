import streamlit as st
import os
import datetime

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import psycopg2
from psycopg2 import Error
import plotly.express as px
import plotly.figure_factory as ff
from pathlib import Path
import plotly.graph_objects as go

# st.set_page_config(
#     page_title="UK House Price",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# with st.sidebar.header("Please input the date:"):
#     start_date = st.sidebar.date_input(
#         "Start Date:",
#         datetime.datetime(2000, 1, 1)
#     )

#     end_date = st.sidebar.date_input(
#         "End Date:",
#         datetime.date(2019, 1, 1)
#     )

#     # try:
#     #     start_date < end_date
#     # except ValueError:
#     #     st.error("Error: End date must fall after start date.")
#     if start_date < end_date:
#         pass
#     else:
#         st.error('Error: End date must fall after start date.')
#     # a_date = st.date_input("Pick a date", min_value=start_date, max_value=end_date)


@st.cache(persist=True, allow_output_mutation=True)
def load_data():
    col1 = ["Average_Price", "Average_Price_SA"]
    col2 = ["Monthly_Change", "Annual_Change"]
    NEW_PATH = os.path.join(Path.cwd().parents[0],"csv_files","house_price")
    DATA_PATH = os.path.join(NEW_PATH, 'Average_price-2022-02_from2000.csv')
    df = pd.read_csv(DATA_PATH)
    df2 = df.drop("Unnamed: 0", axis=1)
    df2["Date"] = pd.to_datetime(df2.Date)
    df2[col1] = df2[col1].astype("float32")
    df2[col2] = df2[col2].astype("float16")
    return df2

def set_linechart(df, region):
    """
    Visualize housing price trend with adjustment on start and end date
    """
    # df2 = df[df['Region_Name']=='England']
    df = df[region]
    line_chart = px.line(df, x="Date", y="Average_Price", title='Average Price')
    line_chart.update_traces(line_color='springgreen', line_width=2)
    st.plotly_chart(line_chart)

def add_goplot(df, region_input):
    # https://www.kaggle.com/code/justinas/house-prices-in-london#4.-House-Prices-Prediction-
    data = df[df['Region_Name']== region_input]
    st.write(data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["Date"], 
                         y=data["Average_Price"],
                         mode='lines',
                         name='Newcastle Average House Price',
                        ))

    fig.update_layout(
    template='gridon',
    title='Average Monthly House Price',
    xaxis_title='Year',
    yaxis_title='Price (£)',
    xaxis_showgrid=False,
    yaxis_showgrid=False,
    legend=dict(y=-.2, orientation='h'),
    shapes=[
        dict(
            type="line",
            x0='2016-06-01',
            x1='2016-06-01',
            y0=0,
            y1=data["Average_Price"].max()*1.2,
            line=dict(
            color="LightSalmon",
            dash="dashdot"
            )
        ),
        dict(
            type="rect",
            x0="2007-12-01",
            y0=0,
            x1="2009-06-01",
            y1=data["Average_Price"].max()*1.2,
            fillcolor="LightSalmon",
            opacity=0.5,
            layer="below",
            line_width=0,
        ),
        dict(
            type="rect",
            x0="2001-03-01",
            y0=0,
            x1="2001-11-01",
            y1=data["Average_Price"].max()*1.2,
            fillcolor="LightSalmon",
            opacity=0.5,
            layer="below",
            line_width=0,
        )
    ],
    annotations=[
        dict(text="Dot-Com Bubble Recession", x='2001-03-01', y=data["Average_Price"].max()*1.2),
        dict(text="The Great Recession", x='2007-12-01', y=data["Average_Price"].max()*1.2),
        dict(text="Brexit Vote", x='2016-06-01', y=data["Average_Price"].max()*1.2)
    ])
    fig.show()


def mask_date(df, start_date, end_date):
    """
    Query dataframe filtered by start and end date
    """
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    mask = (df['Date'] > start_date) & (df['Date'] <= end_date)
    return df[mask]

def percentage_change(df):
    """
    Rate of change taken from max and min average price within given time period
    """
    diff = df['Average_Price'].max() - df['Average_Price'].min()
    return round(100*diff/df['Average_Price'].max(),2)

def app():
    data = load_data()
    # st.subheader('Tabular data')
    # st.write(data)

    ## Filtering
    # Create masks
    region = data['Region_Name'].unique().tolist()

    region_selection = st.multiselect('Region Name:',
                                    region,
                                    default='England')

    region_mask = data['Region_Name'].isin(region_selection)

    start_date = st.sidebar.date_input(
        "Start Date:",
        datetime.datetime(2000, 1, 1)
    )

    end_date = st.sidebar.date_input(
        "End Date:",
        datetime.date(2019, 1, 1)
    )

    # try:
    #     start_date < end_date
    # except ValueError:
    #     st.error("Error: End date must fall after start date.")
    if start_date < end_date:
        pass
    else:
        st.error('Error: End date must fall after start date.')

    add_goplot(data, 'Newcastle upon Tyne')
    data = data[region_mask]
    data_datemask = mask_date(data, start_date, end_date)
    set_linechart(data_datemask, region_mask)
    

    col1, col2, col3 = st.columns(3)
    perc_change = percentage_change(data_datemask)
    col1.metric("Price Max", round(data_datemask['Average_Price'].max(),4))
    col2.metric("Price Min", round(data_datemask['Average_Price'].min(),4))
    col3.metric("Percentage Increase/Decrease", str(perc_change)+'%')

# if __name__ == '__main__':
#     main()