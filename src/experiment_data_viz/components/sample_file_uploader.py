"""src/experiment_data_viz/components/sample_file_uploader.py module."""
import numpy as np
import pandas as pd
import streamlit as st

from streamlit.script_runner import StopException

from experiment_data_viz.bca_analyis import (
    get_concentration_values,
    read_plate_file,
    read_sample_file,
)
from experiment_data_viz.constants import (
    BCA_CONCENTRATION_COLUMN,
    DEFAULT_LEVEL1_COL,
    DEFAULT_LEVEL2_COL,
)


class SampleFileUploader:
    """Custom file uploader class."""

    def __init__(self):
        self._uploaded_sample_file = None
        self._uploaded_plate_file = None
        self._sample_data = pd.DataFrame()
        self._plate_data = pd.DataFrame()
        self._protein_column = None
        self._xaxis_column = None
        self._color_column = None

    def display(self):
        """Display the custom protein uploader."""
        st.sidebar.header("Upload Experiment Data")
        self._uploaded_sample_file = st.sidebar.file_uploader(
            "Choose a Sample file (.csv)"
        )
        if not self._uploaded_sample_file:
            st.subheader("Please upload a Sample file.")
            st.write(
                "Use a .csv exported version of a sheet like this one: https://docs.google.com/spreadsheets/d/1tDpV7IwJx3m6Cs1vGITK4UrvIDU7-e1J8CsrWW_JgEA/edit?usp=sharing"
            )
            raise StopException

        self._sample_data = read_sample_file(sample_filename=self._uploaded_sample_file)
        # Strip all String columns
        df_obj = self._sample_data.select_dtypes(["object"])
        self._sample_data[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
        st.sidebar.write(self._uploaded_sample_file.name)

        self._uploaded_plate_file = st.sidebar.file_uploader(
            "Choose a Plate file (.csv)"
        )
        if self._uploaded_plate_file:
            self._plate_data = read_plate_file(plate_filename=self._uploaded_plate_file)

            self._sample_data, _ = get_concentration_values(
                plate_data=self._plate_data,
                sample_data=self._sample_data,
                number_of_replicates=1,
                sample_start="C1",
                sample_end="C12",
            )
            self._protein_column = BCA_CONCENTRATION_COLUMN

    def display_choice(self):
        """Display the choice for the columns to use."""
        if len(self._sample_data) != 0:
            # try setting default indices if they exist
            try:
                default_index_l1 = int(
                    np.where(self._sample_data.columns == DEFAULT_LEVEL1_COL)[0][0]
                )
            except IndexError:
                default_index_l1 = 0

            try:
                default_index_l2 = int(
                    np.where(self._sample_data.columns == DEFAULT_LEVEL2_COL)[0][0]
                )
            except IndexError:
                default_index_l2 = 0

            try:
                default_protein_col = int(
                    np.where(self._sample_data.columns == BCA_CONCENTRATION_COLUMN)[0][
                        0
                    ]
                )
            except IndexError:
                default_protein_col = 0

            self._protein_column = st.sidebar.selectbox(
                "Select column containing Protein concentration",
                options=list(self._sample_data.columns),
                index=default_protein_col,
                key="protein_col",
            )
            self._xaxis_column = st.sidebar.selectbox(
                "Select 1st level x-axis column",
                options=list(self._sample_data.columns),
                index=default_index_l1,
                key="1st_xaxis_col",
            )
            self._color_column = st.sidebar.selectbox(
                "Select 2nd level x-axis column",
                options=list(self._sample_data.columns),
                index=default_index_l2,
                key="2nd_xaxis_col",
            )

    @property
    def sample_data(self):
        """Getter for sample_data."""
        return self._sample_data

    @property
    def plate_data(self):
        """Getter for plate_data."""
        return self._plate_data

    @property
    def uploaded_files(self):
        """Getter for uploaded_files."""
        return self._uploaded_files

    @property
    def protein_column(self):
        """Getter for protein_column."""
        return self._protein_column

    @property
    def xaxis_column(self):
        """Getter for xaxis_column."""
        return self._xaxis_column

    @property
    def color_column(self):
        """Getter for color_column."""
        return self._color_column
