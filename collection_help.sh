export GOOGLE_APPLICATION_CREDENTIALS=~/.google_cloud/credentials/google_credentials.json

gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS

## Check storage capacity of a certain directory
du -sh /home/rizdi.aprilian/data-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql/ny_taxi_postgres_dataset
du -h