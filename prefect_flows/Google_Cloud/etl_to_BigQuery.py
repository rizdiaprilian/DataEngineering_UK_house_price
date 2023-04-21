from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(log_prints=True, retries=3, retry_delay_seconds=30)
def extract_data_from_gcs(file_name: str) -> Path:
    """Read data from web into pandas DataFrame."""
    gcs_path = Path(f"data/{file_name}.parquet")
    gcs_block = GcsBucket.load("uk-house-price-gcs-block")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data_BigQuery/")
    return Path(f"../data_BigQuery/{gcs_path}")
    

@task(log_prints=True)
def transform_data(path: Path) -> pd.DataFrame:
    """Transform data into a new DataFrame
    Reducing size of dataset using type conversion
    Other preprocessing techniques may apply. 
    """
    df = pd.read_parquet(path)
    # col1 = ["Average_Price", "Average_Price_SA"]
    # col2 = ["Monthly_Change", "Annual_Change"]
    # col3 = ["Sales_Volume"]
    
    # df[col1] = df[col1].astype("float32")
    # df[col2] = df[col2].astype("float16")

    return df

@task(log_prints=True)
def write_bigQuery(df: pd.DataFrame) -> None:
    """Write data to parquet file."""
    
    gcp_credentials_block = GcpCredentials.load("uk-house-price-block")

    df.to_gbq(
        destination_table="UK_house_price_all.first-time-buyer-former-owner-occupied",
        project_id="data-eng-camp-apr22",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=100000,
        if_exists="append",
    )
    return

@flow()
def etl_gcs_to_bq():
    """The main ETL function
    Download data from source repos, transform them, and
    write them to BigQuery Warehouse.
    """
    file_name = "first-time-buyer-former-owner-occupied-2023-01"
    path = extract_data_from_gcs(file_name)
    df = transform_data(path)
    write_bigQuery(df)

if __name__ == "__main__":
    etl_gcs_to_bq()