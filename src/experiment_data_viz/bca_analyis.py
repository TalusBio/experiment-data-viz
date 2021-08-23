"""src/experiment_data_viz/bca_analysis.py module."""
from pathlib import Path

import click
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression

from experiment_data_viz.constants import (
    BCA_CONCENTRATION_COLUMN,
    KNOWN_CONCENTRATIONS,
    ROW_LENGTH,
    STANDARD_BLANK_INDEX,
)


def read_plate_file(plate_filename):
    """Reading the plate file. We only use the first 8 rows because only these contain relevant data."""
    df = pd.read_csv(plate_filename, index_col=0)
    return df.iloc[0:8]


def read_sample_file(sample_filename):
    """Reading the sample file."""
    return pd.read_csv(sample_filename, sep=None)


def subtract_blanks(df_man, blank_pos, df_main):
    """Sub program to subtract the average of the blank in the std curve from each of the samples."""
    blank = float(df_main.iloc[[blank_pos]])
    new_df = df_man.subtract(blank)
    return new_df


def organize_data(df, num_replicates=3):
    # TODO: fix docstring
    """Rearranges data to single"""
    return df.values.flatten().reshape(-1, num_replicates)


def calculate_concentration_values(lin_reg, df):
    """Calculating concentration values using coefficient and intercept from LinearRegression object."""
    coef = float(lin_reg.coef_[0])
    intercept = float(lin_reg.intercept_)
    df = df.multiply(coef)
    df = df.add(intercept)
    return df


def plot_linreg(x, y, y_pred):
    """Plots linear regression."""
    plt.scatter(x, y)
    plt.plot(x, y_pred, color="red")
    plt.show()


def get_plate_index(plate_index, target_index):
    """Calculates the plate index based on a sample index e.g. C1 or B12."""
    row = target_index[0]
    column_value = int(target_index[1:]) - 1
    row_value = plate_index.index(row)
    return row_value * ROW_LENGTH + column_value


def add_BCA_to_sample_data(sample_df, plate_df, sample_start, sample_end):
    """Slices BCA Data to fit the sample table from benchling table. If desired can append to any table though"""
    target_index_start = get_plate_index(
        plate_index=plate_df.index.to_list(), target_index=sample_start
    )
    target_index_end = get_plate_index(
        plate_index=plate_df.index.to_list(), target_index=sample_end
    )
    df_slice = plate_df.values.flatten()[target_index_start : target_index_end + 1]
    sample_df[BCA_CONCENTRATION_COLUMN] = df_slice
    return sample_df


def get_concentration_values(
    plate_data,
    sample_data,
    number_of_replicates,
    sample_start,
    sample_end,
    sample_blank_index=STANDARD_BLANK_INDEX,
):
    """Calculates concentration values from the plate data and sample data."""
    # Perform linear regression of BCA STD
    df_std = plate_data.iloc[[0, 1]]
    df_avg = df_std.mean(axis=0)

    # Subtract the blanks from our training data set x
    df_x = subtract_blanks(
        df_man=df_avg, blank_pos=STANDARD_BLANK_INDEX, df_main=df_avg
    )

    x = df_x.iloc[: STANDARD_BLANK_INDEX + 1].values
    x = x.reshape([-1, 1])
    lin_reg = LinearRegression()
    lin_reg.fit(x, KNOWN_CONCENTRATIONS)
    # y_pred = lin_reg.predict(x)
    # plot_linreg(x=x, y=KNOWN_CONCENTRATIONS, y_pred=y_pred)

    # Takes subsection of orginial file excluding std curve samples
    plate_data_rest = plate_data.iloc[2:]

    plate_data_rest = subtract_blanks(
        df_man=plate_data_rest, blank_pos=sample_blank_index, df_main=df_avg
    )

    plate_data_rest = calculate_concentration_values(
        lin_reg=lin_reg, df=plate_data_rest
    )

    # drop NaN values
    plate_data_rest = plate_data_rest.dropna()

    df_sample = add_BCA_to_sample_data(
        sample_df=sample_data,
        plate_df=plate_data_rest,
        sample_start=sample_start,
        sample_end=sample_end,
    )

    # organizes data into side by side replicates for easy averaging and plotting on prism
    protein_arr = organize_data(df=plate_data_rest, num_replicates=number_of_replicates)

    return df_sample, protein_arr


@click.command()
@click.option("-f", "--plate_filename", help="Name of the file to process.")
@click.option(
    "-s", "--sample_filename", help="Name of the file containing the sample metadata."
)
@click.option(
    "-r",
    "--number_of_replicates",
    default=1,
    type=int,
    help="Number of replicates each sample has.",
)
@click.option("--sample_start", type=str, default="C1", help="")
@click.option("--sample_end", type=str, default="H12", help="")
@click.option("--sample_blank_index", type=int, default=STANDARD_BLANK_INDEX, help="")
def main(
    plate_filename,
    sample_filename,
    number_of_replicates,
    sample_start,
    sample_end,
    sample_blank_index,
):
    plate_data = read_plate_file(plate_filename=plate_filename)
    sample_data = read_sample_file(sample_filename=sample_filename)

    df_sample, protein_arr = get_concentration_values(
        plate_data=plate_data,
        sample_data=sample_data,
        number_of_replicates=number_of_replicates,
        sample_start=sample_start,
        sample_end=sample_end,
        sample_blank_index=sample_blank_index,
    )

    df_sample.to_csv(
        f"{Path(sample_filename).with_suffix('').stem}_{sample_start}_{sample_end}.csv",
        index=None,
    )
    np.savetxt(f"protein_{plate_filename}", protein_arr, delimiter=",")
