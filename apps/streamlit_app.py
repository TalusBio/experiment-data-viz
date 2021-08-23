"""apps/streamlit_app.py module."""
import plotly.express as px
import streamlit as st

from experiment_data_viz.components import file_uploader
from experiment_data_viz.utils import (
    get_table_download_link,
    streamlit_static_downloads_folder,
)


TITLE = "Experiment Data Viz"

st.set_page_config(
    page_title=TITLE,
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    st.title(TITLE)

    downloads_path = streamlit_static_downloads_folder()

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

    st.subheader("Edit Output DataFrame")
    sample_data_edit = sample_data.copy(deep=True)

    postfix = st.text_input("Postfix")
    column = st.selectbox("Column to apply", options=sample_data.columns)
    columns_to_keep = st.multiselect(
        "Select Columns to keep",
        options=list(sample_data.columns),
        default=list(sample_data.columns),
    )
    if postfix:
        sample_data_edit[column] = sample_data_edit[column].apply(
            lambda x: f"{x}_{postfix}"
        )
        sample_data_edit = sample_data_edit[columns_to_keep]
    st.dataframe(sample_data_edit)

    st.markdown(
        get_table_download_link(df=sample_data_edit, downloads_path=downloads_path),
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
