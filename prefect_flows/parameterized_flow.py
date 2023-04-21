import os
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch_parquet(url):
    if url.endswith('.parquet.gz'):
        parquet_file = url
    else:
        parquet_file = url
        parquet_file = parquet_file.split("/")[-1]
    print(f"Downloading {parquet_file} to container service...")
    ## Download file from source portal and save it to out machine
    os.system(f"wget {url} -O {parquet_file}")
    print(f"Download completed. Now reading a parquet file...")
    df = pd.read_parquet(parquet_file)
    return df


@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    current_dir = os.getcwd()
    path = os.path.join(current_dir, "data")
    path = Path(f"{path}/{color}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    return path


@task()
def write_gcs(path: Path, dataset_file: str) -> None:
    """Upload local parquet file to GCS"""
    gcs_path = Path(f"data/{dataset_file}.parquet")
    gcs_block = GcsBucket.load("uk-house-price-gcs-block")
    gcs_block.upload_from_path(from_path=path, to_path=gcs_path)
    return


@flow()
def etl_web_to_gcs(year: int, month: int, color: str) -> None:
    """The main ETL function"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    df = fetch_parquet(f"https://d37ci6vzurychx.cloudfront.net/trip-data/{dataset_file}.parquet")
    df_clean = clean(df)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path, dataset_file)

@flow()
def etl_parent_flow(
    months: list[int] = [3, 4], year: int = 2022, color: str = "yellow"
):
    for month in months:
        etl_web_to_gcs(year, month, color)


if __name__ == "__main__":
    color = "yellow"
    months = [3, 4, 5]
    year = 2022
    etl_parent_flow(months, year, color)