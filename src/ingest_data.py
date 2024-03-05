import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os
import sys
from pathlib import Path
import argparse

MAIN_DIR = Path(os.getcwd()).parent

def download_parquet(url, parquet_file: str):

    os.system(f"wget {url} -O {parquet_file}.parquet")
    

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    parquet_file = params.parquet_file

    download_parquet(url, parquet_file)

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

#     df.head(0).to_sql(name={table_name}, con=engine, if_exists="replace", index=False)
#     df.to_sql(name={table_name}, con=engine, if_exists="append", index=False)


# data = os.path.join(MAIN_DIR, "datasets", "NYC_taxi", "green_tripdata_2023-01.parquet")
# df = pd.read_parquet(data, engine="pyarrow")

# engine = create_engine("postgresql://root:root@localhost:5432/ny_taxi")
# engine.connect()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest parquet data to PostgreSQL")

    parser.add_argument("--user", help="user name for postgresql")
    parser.add_argument("--password", help="password for postgresql")
    parser.add_argument("--host", help="host for postgresql")
    parser.add_argument("--port", help="port for postgresql")
    parser.add_argument("--db", help="db for postgresql")
    parser.add_argument("--table_name", help="name of the table about to be ingested to PostgreSQL")
    parser.add_argument("--url", help="url of the parquet file")
    parser.add_argument("--parquet_file", help="parquet file")

    args = parser.parse_args()

    main(args)

