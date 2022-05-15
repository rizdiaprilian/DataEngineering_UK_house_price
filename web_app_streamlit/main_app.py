import streamlit as st
from multipage import MultiApp
from apps import pandas_profiling_uk_houseprice, web_app_uk_houseprice

app = MultiApp()

st.set_page_config(
    page_title="UK House Price",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
# UK House Price App
With the launch of Streamlit, developing a dashboard for your machine learning solution has been made incredibly easy.

Streamlit is an open source app framework specifically designed for ML engineers working with Python. 
It allows you to create a stunning looking application with only a few lines of code.

I want to take this opportunity to demonstrate the apps you can build using Streamlit. 
""")

# Add all your application here
app.add_app("Pandas Profiling UK Houseprice", pandas_profiling_uk_houseprice.app)
app.add_app("Trend UK Houseprice", web_app_uk_houseprice.app)
# app.add_app("Statistical Model", model.app)
# The main app
app.run()