import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


TITLE = "Experiment Data Viz"

st.set_page_config(
    page_title=TITLE,
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title(TITLE)

st.sidebar.title("Upload Experiment Data")
uploaded_file = st.sidebar.file_uploader("Upload a file (.csv)")

if uploaded_file:
    df = pd.read_csv(uploaded_file, sep=None)
    st.sidebar.write(uploaded_file.name)

    # strip all string columns
    df_obj = df.select_dtypes(["object"])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

    WIDTH = 1000
    HEIGHT = 900
    DEFAULT_LEVEL1_COL = "Cell Type"
    DEFAULT_LEVEL2_COL = "Method (KF or manual)"
    DEFAULT_PROTEIN_COL = "BCA (ug/ul, Bound Protein)"

    # try setting default indices if they exist
    try:
        default_index_l1 = int(np.where(df.columns == DEFAULT_LEVEL1_COL)[0][0])
    except:
        default_index_l1 = None

    try:
        default_index_l2 = int(np.where(df.columns == DEFAULT_LEVEL2_COL)[0][0])
    except:
        default_index_l2 = None

    try:
        default_protein_col = int(np.where(df.columns == DEFAULT_PROTEIN_COL)[0][0])
    except:
        default_protein_col = None

    protein_col = st.sidebar.selectbox(
        "Select column containing Protein concentration",
        options=list(df.columns),
        index=default_protein_col,
        key="protein_col",
    )
    xaxis_col = st.sidebar.selectbox(
        "Select 1st level x-axis column",
        options=list(df.columns),
        index=default_index_l1,
        key="1st_xaxis_col",
    )
    color_col = st.sidebar.selectbox(
        "Select 2nd level x-axis column",
        options=list(df.columns),
        index=default_index_l2,
        key="2nd_xaxis_col",
    )

    fig = px.box(
        df, x=xaxis_col, y=protein_col, color=color_col, width=WIDTH, height=HEIGHT
    )
    st.subheader("Box Plot showing Protein Concentration (ug/ul)")
    st.write(fig)

    st.subheader("Input DataFrame")
    st.dataframe(df)

else:
    st.subheader("Please upload a file.")
    st.write(
        "Use a .csv exported version of a sheet like this one: https://docs.google.com/spreadsheets/d/1tDpV7IwJx3m6Cs1vGITK4UrvIDU7-e1J8CsrWW_JgEA/edit?usp=sharing"
    )
