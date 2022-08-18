import pandas as pd
from sqlalchemy.engine import create_engine
from calx.utils import read_file


def read_database(uri: str, query: str) -> pd.DataFrame:
    engine = create_engine(uri)
    return pd.read_sql(query, engine)


def read_database_from_file(
    uri: str, query_file: str, query_param: dict
) -> pd.DataFrame:
    query = read_file(query_file).format(query_param)
    return read_database(uri, query)
