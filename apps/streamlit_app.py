"""apps/streamlit_app.py module."""
import plotly.express as px
import streamlit as st

from experiment_data_viz.components import file_uploader


TITLE = "Experiment Data Viz"

st.set_page_config(
    page_title=TITLE,
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    st.title(TITLE)

    plate_uploader = file_uploader.PlateFileUploader()
    plate_uploader.display()
    if not plate_uploader.data.empty:
        plate_uploader.display_choice()

    sample_uploader = file_uploader.SampleFileUploader(
        plate_data_uploader=plate_uploader
    )
    sample_uploader.display()

    sample_data = sample_uploader.data
    if not sample_data.empty:
        sample_uploader.display_choice()

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
