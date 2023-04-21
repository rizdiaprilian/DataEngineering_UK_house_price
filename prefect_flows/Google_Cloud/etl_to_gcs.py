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
    df["Date"] = pd.to_datetime(df.Date)   

    return df

@task(log_prints=True)
def write_parquet(df: pd.DataFrame, dataset_file: str):
    """Write data to parquet file."""
    current_dir = os.getcwd()
    path = os.path.join(current_dir, "data")
    path = Path(f"{path}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    return path

@task(log_prints=True)
def load_data_to_gcs(path: Path, dataset_file: str) -> None:
    """Write parquet file to GCS."""
    gcs_path = Path(f"data/{dataset_file}.parquet")
    gcp_cloud_storage_bucket_block = GcsBucket.load("uk-house-price-gcs-block")
    gcp_cloud_storage_bucket_block.upload_from_path(
        from_path=f"{path}", 
        to_path=gcs_path
        )
    return


@flow()
def etl_web_to_gcs() -> None:
    """The main ETL function
    Download data from source repos, transform them, and
    write them to GCS.
    """
    url_link = "http://publicdata.landregistry.gov.uk/market-trend-data/house-price-index-data/First-Time-Buyer-Former-Owner-Occupied-2023-01.csv"
    file_name = "first-time-buyer-former-owner-occupied-2023-01"

    df = extract_data(file_name, url_link)
    data = transform_data(df)
    path = write_parquet(data, file_name)
    load_data_to_gcs(path, file_name)

if __name__ == "__main__":
    etl_web_to_gcs()