import os
import logging

import pandas
import urllib.parse

from sqlalchemy import create_engine

DB_URL_ENVAR_NAME = "DB_URL"
DB_NAME = "my_db"


class EnvironmentVariableNotDefinedException(Exception):
    pass


def get_db_info() -> urllib.parse.ParseResultBytes:
    """
    Get ParseResultBytes object to connect to database
    """
    urllib.parse.uses_netloc.append("postgres")

    # Raising an exception if 'DB_URL' envvar is not defined.
    if not os.environ.get(DB_URL_ENVAR_NAME, None):
        raise EnvironmentVariableNotDefinedException(
            f"Environment variable (DB_URL) not defined."
        )

    db_info = urllib.parse.urlparse(os.environ.get(DB_URL_ENVAR_NAME))

    return db_info


def post_to_db(df: pandas.core.frame.DataFrame) -> None:
    """
    Pushing dataframe to database
    """
    db_info = get_db_info()

    engine = create_engine(
        f"postgresql://{db_info.username}:{db_info.password}@{db_info.hostname}/{db_info.path[1:]}"
    )

    # Pushing to db
    df.to_sql(DB_NAME, engine, if_exists="replace", index=False)
