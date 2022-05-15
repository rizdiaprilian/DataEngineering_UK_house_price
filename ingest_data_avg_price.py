import os
import argparse
import pandas as pd
from sqlalchemy import create_engine
from time import time


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = "output.csv"
    # download the csv
    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    # It is recommended to divide ny_taxi dataset to into chunks/smaller batches
    col1 = ["Average_Price", "Average_Price_SA"]
    col2 = ["Monthly_Change", "Annual_Change"]
    df_iter = pd.read_csv(
        "./csv_files/house_price/Average_price-2019-12_from2000.csv",
        iterator=True,
        chunksize=20000,
    )
    df2 = next(df_iter)

    df2 = df2.drop("Unnamed: 0", axis=1)
    df2["Date"] = pd.to_datetime(df2.Date)
    df2[col1] = df2[col1].astype("float32")
    df2[col2] = df2[col2].astype("float16")

    ## Create new table "yellow_taxi_data"
    df2.head(0).to_sql(name="avg_price", con=engine, if_exists="replace")

    # Check on pgcli if the table "yellow_taxi_data" has already been made
    df2.to_sql(name="avg_price", con=engine, if_exists="append")

    ### Fill next chunks to "yellow_taxi_data"
    while True:
        try:
            t_start = time()
            df2 = next(df_iter)
            df2 = df2.drop("Unnamed: 0", axis=1)
            df2["Date"] = pd.to_datetime(df2.Date)
            df2[col1] = df2[col1].astype("float32")
            df2[col2] = df2[col2].astype("float16")
            df2.to_sql(name="avg_price", con=engine, if_exists="append")
            t_end = time()
            elapsed = round(t_end - t_start, 4)
            print(f"Inserted another chunk, ... took {elapsed} seconds.")
        except ValueError:
            print("Oops! Inserting chunk failed. Abort immediately...")
        except StopIteration:
            print(f"finished ingesting data into the postgres database.")
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to postgres")

    parser.add_argument("--user", help="user name for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--db", help="database name for postgres")
    parser.add_argument(
        "--table_name", help="name of the table where the results are written to"
    )
    parser.add_argument("--url", help="url of the csv file")

    args = parser.parse_args()

    main(args)
