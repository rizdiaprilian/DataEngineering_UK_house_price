import streamlit as st
import os, datetime
import pandas as pd
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
from pathlib import Path


# st.set_page_config(
#     page_title="UK House Price with Pandas Profiling",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

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

def app():
    df = load_data()
    # pr = gen_profile_report(df, explorative=True)
    st.write(df)
    # pr = df.profile_report()

    # st_profile_report(pr)

    # with st.expander("REPORT", expanded=True):
    #     st_profile_report(df)

# if __name__ == "__main__":
#     main()