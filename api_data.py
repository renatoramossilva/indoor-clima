import json

from sodapy import Socrata

# Data obtained from: https://dev.socrata.com/foundry/analisi.transparenciacatalunya.cat/irki-p3c7
DATASET_ID = "analisi.transparenciacatalunya.cat"
APP_TOKEN = "irki-p3c7"


def get_data_from_api(limit: int = 0) -> list:
    """
    Function to obtain data from 'analisi.transparenciacatalunya.cat'

    'limit' variable defines how many entries will be loaded.
    If no value is passed to 'limit', it gets all the entries
    """
    client = Socrata(DATASET_ID, None)

    if not limit:
        limit = client.get(APP_TOKEN, select="COUNT(*)")[0]["COUNT"]

    response = client.get(APP_TOKEN, limit=limit)

    return response
