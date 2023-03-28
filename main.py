#!/usr/bin/python3

import argparse
import os
import logging
import logging.config

import pandas

import api_data
import db_client


BASE_VALUES = ["data", "comarca"]
DEFAULT_VALUES = BASE_VALUES + ["dosi"]
COLUMNS_NAME = [
    "sexe_codi",
    "sexe",
    "provincia_codi",
    "provincia",
    "comarca_codi",
    "comarca",
    "municipi_codi",
    "municipi",
    "districte",
    "dosi",
    "data",
    "fabricant",
    "recompte",
]

logging.config.fileConfig("logging.conf")
# Set logger
logger = logging.getLogger("indoor_clima")


def get_parser() -> argparse.ArgumentParser:
    """
    Return the argument parser.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--column",
        "-c",
        action="append",
        choices=COLUMNS_NAME,
        required=False,
        help="Option to include an additional column to the dataframe",
    )

    parser.add_argument(
        "--sort",
        "-s",
        default="data",
        choices=COLUMNS_NAME,
        required=False,
        help="Increase output verbosity",
    )

    parser.add_argument(
        "--limit",
        "-l",
        default=0,
        required=False,
        help="Get number of results",
    )
    return parser


def filter_columns(df, args: list = []) -> pandas.core.frame.DataFrame:
    """
    Filter dataframe according to the given values.

    By default, the dataframe includes the values defined in 'DEFAULT_VALUES'
    and additional columns may be added through args.
    """
    if args:
        DEFAULT_VALUES.extend(args)

    logger.info("Show columns: %s", ", ".join([column for column in DEFAULT_VALUES]))
    return df[list(set(DEFAULT_VALUES))]


def filter_dosi(
    df: pandas.core.frame.DataFrame, no_dosi: str = "1"
) -> pandas.core.frame.DataFrame:
    """
    Filter dataframe according to X vaccine doses. Default value is "1"
    e.g.
        x = "1" means 1st dose
        x = "2" means 2nd dose
        (...)
    """
    return df[df["dosi"] == no_dosi]


def sort_data(
    df: pandas.core.frame.DataFrame, criteria: str = "data"
) -> pandas.core.frame.DataFrame:
    """
    Sort dataframe according to the given criteria. Default value is 'data'
    """
    logger.info("Sorting values by %s", criteria)
    return df.sort_values(by=criteria)


def main() -> None:
    # Get all cli arguments
    parser = get_parser()
    args = parser.parse_args()

    # Append extra columns to the 'BASE_VALUES'
    global BASE_VALUES
    if args.column:
        BASE_VALUES.extend(args.column)

    logger.info("Colleting data from transparenciacatalunya.cat")

    # Import data from the API
    results = api_data.get_data_from_api(args.limit)

    # Convert data to pandas DataFrame
    results_df = pandas.DataFrame.from_records(results)
    df = filter_columns(results_df, args=args.column)

    # Creating a new column (n_doses) counting the
    # number of doses per 'date/comarca' and dropping
    # 'dosi' column
    df = (
        pandas.core.frame.DataFrame(
            {"n_doses": filter_dosi(df).groupby(BASE_VALUES)["dosi"].value_counts()}
        )
        .reset_index()
        .drop("dosi", axis=1)
    )

    # Push to database
    db_client.post_to_db(sort_data(df, args.sort))


if __name__ == "__main__":
    main()
