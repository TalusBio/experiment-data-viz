"""src/experiment_data_viz/utils.py"""
import os
import uuid

from pathlib import Path
from shutil import rmtree

import pandas as pd
import streamlit as st


def streamlit_static_downloads_folder() -> Path:
    """Create a downloads directory within the streamlit static asset directory.
    HACK: This only works when we've installed streamlit with pipenv,
    so the permissions during install are the same as the running process.

    Returns
    -------
    Path
        The path to the downloads directory.
    """
    streamlit_static_path = Path(st.__path__[0]).joinpath("static")
    downloads_path = streamlit_static_path.joinpath("downloads")
    if downloads_path.exists():
        rmtree(downloads_path)
    downloads_path.mkdir()
    return downloads_path


def get_table_download_link(df: pd.DataFrame, downloads_path: Path) -> str:
    """Create a table download link for a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe to download.
    downloads_path : Path
        The path to the downloads directory.

    Returns
    -------
    str
        The download link for the data.
    """
    temp_file_path = downloads_path.joinpath(f"{str(uuid.uuid4())}.csv")
    df.to_csv(temp_file_path)
    return f"[Download as .csv file](downloads/{os.path.basename(temp_file_path)})"
