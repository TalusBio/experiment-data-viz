"""apps/streamlit_app.py module."""
import plotly.express as px
import streamlit as st

from experiment_data_viz.components import sample_file_uploader


TITLE = "Experiment Data Viz"

st.set_page_config(
    page_title=TITLE,
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    st.title(TITLE)

    sample_uploader = sample_file_uploader.SampleFileUploader()
    sample_uploader.display()

    sample_data = sample_uploader.sample_data
    if not sample_data.empty:
        sample_uploader.display_choice()

    # strip all string columns
    df_obj = sample_data.select_dtypes(["object"])
    sample_data[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

    WIDTH = 1000
    HEIGHT = 900

    fig = px.box(
        sample_data,
        x=sample_uploader.xaxis_column,
        y=sample_uploader.protein_column,
        color=sample_uploader.color_column,
        width=WIDTH,
        height=HEIGHT,
    )
    st.subheader("Box Plot showing Protein Concentration (ug/ul)")
    st.write(fig)

    st.subheader("Input DataFrame")
    st.dataframe(sample_data)


if __name__ == "__main__":
    main()
