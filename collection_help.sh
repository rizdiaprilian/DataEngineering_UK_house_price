export GOOGLE_APPLICATION_CREDENTIALS=~/.google_cloud/credentials/google_credentials.json

gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS

## Check storage capacity of a certain directory
du -sh /home/rizdi.aprilian/data-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql/ny_taxi_postgres_dataset
du -h

## Creating docker network and volume to link together pg-database and pg-admin
docker network create pg-network

docker volume create --name dtc_postgre_volumne_local -d local 

docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v dtc_postgre_volumne_local:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13

docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pg-admin \
    dpage/pgadmin4

### Converting jupyter format to python format
jupyter nbconvert --to=script

URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2023-02.parquet"

python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=green_trip_data_february \
    --url=${URL} \
    --parquet_file=green_feb