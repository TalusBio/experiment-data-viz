"""tests/test_bca_analysis.py module."""
from pathlib import Path

import pandas as pd

from numpy.testing import assert_array_almost_equal
from pandas.testing import assert_frame_equal

from experiment_data_viz import bca_analyis


DATA_DIR = Path(__file__).resolve().parent.joinpath("data")

PLATE_FILE_KEY = DATA_DIR.joinpath("Gryder_P2_7Jul21.csv")
SAMPLE_FILE_KEY = DATA_DIR.joinpath("Sample 1.csv")

PROTEINS_EXPECTED = pd.read_csv(
    DATA_DIR.joinpath("protein_Gryder_P2_7Jul21.csv"), header=None
)
SAMPLE_EXPECTED = pd.read_csv(DATA_DIR.joinpath("Sample 1.csv_C1_C12.csv"))


def test_end_to_end() -> None:
    """Test end to end."""
    plate_data = bca_analyis.read_plate_file(plate_filename=PLATE_FILE_KEY)
    sample_data = bca_analyis.read_sample_file(sample_filename=SAMPLE_FILE_KEY)

    df_sample_actual, protein_arr_actual = bca_analyis.get_concentration_values(
        plate_data=plate_data,
        sample_data=sample_data,
        number_of_replicates=1,
        sample_start="C1",
        sample_end="C12",
    )

    assert_frame_equal(df_sample_actual, SAMPLE_EXPECTED)
    assert_array_almost_equal(protein_arr_actual, PROTEINS_EXPECTED)
