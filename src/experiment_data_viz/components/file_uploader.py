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
    DEFAULT_NUM_REPLICATES,
    DEFAULT_SAMPLE_END,
    DEFAULT_SAMPLE_START,
    STANDARD_BLANK_INDEX,
)


class SampleFileUploader:
    """Custom sample file uploader class."""

    def __init__(self, plate_data_uploader):
        self._uploaded_file = None
        self._data = pd.DataFrame()
        self._plate_data_uploader = plate_data_uploader
        self._protein_column = None
        self._xaxis_column = None
        self._color_column = None

    def display(self):
        """Display the custom protein uploader."""
        st.sidebar.header("Upload Sample Data")
        self._uploaded_file = st.sidebar.file_uploader(
            "Choose a Sample Information file (.csv)"
        )
        if not self._uploaded_file:
            st.subheader("Please upload a Sample Information file.")
            st.write(
                "Use a .csv exported version of a sheet like this one: https://docs.google.com/spreadsheets/d/1tDpV7IwJx3m6Cs1vGITK4UrvIDU7-e1J8CsrWW_JgEA/edit?usp=sharing"
            )
            raise StopException

        self._data = read_sample_file(sample_filename=self._uploaded_file)
        # Strip all String columns
        df_obj = self._data.select_dtypes(["object"])
        self._data[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
        st.sidebar.write(self._uploaded_file.name)

        if (
            isinstance(self._plate_data_uploader, PlateFileUploader)
            and not self._plate_data_uploader.data.empty
        ):
            self._data, _ = get_concentration_values(
                plate_data=self._plate_data_uploader.data,
                sample_data=self._data,
                number_of_replicates=self._plate_data_uploader.num_replicates,
                sample_start=self._plate_data_uploader.sample_start,
                sample_end=self._plate_data_uploader.sample_end,
                sample_blank_index=self._plate_data_uploader.sample_blank_index,
            )

    def display_choice(self):
        """Display the choice for the columns to use."""
        if len(self._data) != 0:
            # try setting default indices if they exist
            try:
                default_index_l1 = int(
                    np.where(self._data.columns == DEFAULT_LEVEL1_COL)[0][0]
                )
            except IndexError:
                default_index_l1 = 0

            try:
                default_index_l2 = int(
                    np.where(self._data.columns == DEFAULT_LEVEL2_COL)[0][0]
                )
            except IndexError:
                default_index_l2 = 0

            try:
                default_protein_col = int(
                    np.where(self._data.columns == BCA_CONCENTRATION_COLUMN)[0][0]
                )
            except IndexError:
                default_protein_col = 0

            self._protein_column = st.sidebar.selectbox(
                "Select column containing Protein concentration",
                options=list(self._data.columns),
                index=default_protein_col,
                key="protein_col",
            )
            self._xaxis_column = st.sidebar.selectbox(
                "Select 1st level x-axis column",
                options=list(self._data.columns),
                index=default_index_l1,
                key="1st_xaxis_col",
            )
            self._color_column = st.sidebar.selectbox(
                "Select 2nd level x-axis column",
                options=list(self._data.columns),
                index=default_index_l2,
                key="2nd_xaxis_col",
            )

    @property
    def data(self):
        """Getter for data."""
        return self._data

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

    @property
    def plate_data_uploader(self):
        """Getter for plate_data_uploader."""
        return self._plate_data_uploader

    @plate_data_uploader.setter
    def plate_data_uploader(self, value):
        self._plate_data_uploader = value


class PlateFileUploader:
    """Custom plate file uploader class."""

    def __init__(self):
        self._uploaded_file = None
        self._data = pd.DataFrame()
        self._num_replicates = DEFAULT_NUM_REPLICATES
        self._sample_start = DEFAULT_SAMPLE_START
        self._sample_end = DEFAULT_SAMPLE_END
        self._sample_blank_index = STANDARD_BLANK_INDEX

    def display(self):
        """Display the custom protein uploader."""
        st.sidebar.header("Upload BCA Data")
        self._uploaded_plate_file = st.sidebar.file_uploader("Choose a BCA file (.csv)")
        if self._uploaded_plate_file:
            self._data = read_plate_file(plate_filename=self._uploaded_plate_file)

    def display_choice(self):
        """Display the choice for the columns to use."""
        if len(self._data) != 0:
            self._num_replicates = st.sidebar.number_input(
                "Number of Replicates Used", value=DEFAULT_NUM_REPLICATES
            )
            self._sample_start = st.sidebar.text_input(
                "Sample Start", value=DEFAULT_SAMPLE_START
            )
            self._sample_end = st.sidebar.text_input(
                "Sample End", value=DEFAULT_SAMPLE_END
            )
            self._sample_blank_index = st.sidebar.number_input(
                "Sample Blank Index", value=STANDARD_BLANK_INDEX
            )

    @property
    def data(self):
        """Getter for data."""
        return self._data

    @property
    def num_replicates(self):
        """Getter for num_replicates."""
        return self._num_replicates

    @property
    def sample_start(self):
        """Getter for sample_start."""
        return self._sample_start

    @property
    def sample_end(self):
        """Getter for sample_end."""
        return self._sample_end

    @property
    def sample_blank_index(self):
        """Getter for sample_start_index."""
        return self._sample_blank_index
