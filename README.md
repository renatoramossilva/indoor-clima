Back-end test - Indoor Clima
====================

# General

## Database
ElephantSQL: `https://www.elephantsql.com/`

## Code
The code is organised in 5 files

* `requirements.txt`: List of all modules/packages required to this project

* `main.py`: This file contains the logic required for the test and some
extra important informations, such as:
    - Input arguments definition
    - Global variables
    - Log Configuration

* `api_data.py`: Interface to obtain data to be analyzed from 'analisi.transparenciacatalunya.cat'

* `db_client.py`: Interface to push dataframe to database

* `logging.conf`: Log configuration file

The following instructions may be useful:

# Install requirements
Install all Python modules and packages listed in your requirements.txt

    pip install -r requirements.txt

# Launch the script

It is possible to use input arguments to improve the data analysis visualization.

Further information runs:

    python main -h

## Examples

### Add Columns
By default the columns presented are: "data", "comarca" and "n_doses".

```
                      data          comarca  n_doses
0  2021-04-01T00:00:00.000   ALTA RIBAGORÇA        1
1  2021-04-01T00:00:00.000  VALLES ORIENTAL        1
2  2021-05-14T00:00:00.000   No classificat        1
3  2021-06-28T00:00:00.000      ALT EMPORDA        1
4  2022-01-07T00:00:00.000         BERGUEDA        1

```

To add other columns in the database, please use --column/-c as input argument

e.g.

    python3 main.py -c "sexe"

```
                     data          comarca  sexe  n_doses
0  2021-04-01T00:00:00.000   ALTA RIBAGORÇA  Home        1
1  2021-04-01T00:00:00.000  VALLES ORIENTAL  Home        1
2  2021-05-14T00:00:00.000   No classificat  Home        1
3  2021-06-28T00:00:00.000      ALT EMPORDA  Home        1
4  2022-01-07T00:00:00.000         BERGUEDA  Home        1
```

### Sorting dataframe
By default, the values are sorted by "date". To sort the dataframe in database using other criteria, you might use the argument --sort/-s.

e.g.

    python3 main.py --sort "comarca"

```
                      data          comarca  n_doses
5  2021-06-28T00:00:00.000      ALT EMPORDA        1
0  2021-04-01T00:00:00.000   ALTA RIBAGORÇA        1
6  2021-09-08T00:00:00.000            BAGES        1
7  2022-01-07T00:00:00.000         BERGUEDA        1
4  2021-05-14T00:00:00.000   No classificat        1
3  2021-05-05T00:00:00.000         SOLSONES        1
1  2021-04-01T00:00:00.000  VALLES ORIENTAL        1
2  2021-04-15T00:00:00.000  VALLES ORIENTAL        1
```

### Limit of results

Using this argument, your can define how many inputs will be obtained from
the API. If no value is passed for this argument, the script gets all the
records.

e.g.

    python3 main.py --limit 3

```
                      data          comarca  n_doses
0  2021-04-01T00:00:00.000  VALLES ORIENTAL        1
1  2021-05-14T00:00:00.000   No classificat        1
2  2021-06-28T00:00:00.000      ALT EMPORDA        1
```