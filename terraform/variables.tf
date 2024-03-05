locals {
  data_lake_bucket = "dtc_data_lake"
}

variable "project" {
  description = "Your GCP Project ID"
  default = "data-eng-camp-apr22"
  type = string
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "europe-west6"
  type = string
}

variable "bucket_name" {
  description = "The name of the GCS bucket. Must be globally unique."
  default = "bucket_DE_2024"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "Mage_data_engineer"
  # type = list
  # default = ["UK_house_price_staging", "UK_house_price_development", "UK_house_price_production"]
}
