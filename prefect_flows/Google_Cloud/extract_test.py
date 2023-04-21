import os
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
from prefect_gcp.cloud_storage import GcsBucket

@task(log_prints=True, tags=["extract"], cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(file_name: str, url: str) -> pd.DataFrame:
    """Read data from web into pandas DataFrame."""
    current_dir = os.getcwd()
    csv_name=f"{file_name}.csv"
    path = os.path.join(current_dir, "data", csv_name)
    os.system(f"wget {url} -O {path}")
    df = pd.read_csv(
        path
    )

    return df

@task(log_prints=True)
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform data into a new DataFrame
    Reducing size of dataset using type conversion
    Other preprocessing techniques may apply. 
    """
    print("Data before type conversion ")
    print(df.info())

    col1 = ["Average_Price", "Average_Price_SA"]
    col2 = ["Monthly_Change", "Annual_Change"]

    
    df["Date"] = pd.to_datetime(df.Date)
    # df[col1] = df[col1].astype("float32")
    # df[col2] = df[col2].astype("float16")
    print("Data after type conversion ")
    print(df.info())

    return df

@task(log_prints=True)
def write_parquet(df: pd.DataFrame, dataset_file: str):
    """Write data to parquet file."""
    current_dir = os.getcwd()
    path = os.path.join(current_dir, "data")
    path = Path(f"{path}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    return path

@flow()
def etl_web_to_gcs() -> None:
    """The main ETL function
    Download data from source repos, transform them, and
    write them to GCS.
    """
    url_link = "http://publicdata.landregistry.gov.uk/market-trend-data/house-price-index-data/Average-prices-2023-01.csv"
    file_name = "average_price-2023-01"

    df = extract_data(file_name, url_link)
    data = transform_data(df)
    path = write_parquet(data, file_name)



if __name__ == "__main__":
    etl_web_to_gcs()