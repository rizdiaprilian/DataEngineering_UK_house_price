# Data Engineering_UK_house_price

### Overview
This project implements data engineering practices to discover changes of housing market price across the UK, hence contributing to a better understanding of the UK housing market and provide insights that can inform decision-making in the real estate sector.  

### Problem Statement
The surging rise of housing market prices in the UK has been influencing the country's economy. Many questions surround the factors that possibly contribute
to this rise. Examining the relationships between average price, annual change, location, property type, we want to exploit any insight how their dynamic change
affect consumer purchase capability.



#### About the Dataset

The UK house price index (UK HPI) data consists of calculation results of data gathered from HM Land Registry, Registers of Scotland, Land and Property Service Northern Ireland. Updates on data take place in monthly basis, while figures derived from Northern Ireland are updated quarterly. This data is made publicly available with some considerations in mind:
- Low number of sales transactions in some local authorities may lead to volatility in the estimates.
- The UK HPI is calculated based on actual completed sales, rather than advertised or approved prices, which results in a delay in its publication compared to  other house price index in the UK. The reason for this is that the UK HPI is only available at the end of the conveyancing process, when the sale of a property is completed.

The dataset contains the sale price of the property, sales completion date, full address details, property types (detached, semi-detached, terraced or flat), newly built or established residential building, financed or non-financed transaction.

This data is organised under approvement of HM Land Registry.


### Objectives

Build a foundation of data architecture that accomodate data warehouse for storage and large-scale processing.
Establish data ingestion and pipeline that allow extraction from source repository in scheduled manner.
Provide a dashboard for presenting visual outlook of the price movement.

### Technologies

All of development is brought on within Anaconda environment. Project structure has been set with tools :
For setting up the VM Instance or Local Machine I installed these tools:

- Terraform
- Google Cloud Platform: Google Cloud Storage, BigQuery, Google Compute Engine
- Prefect
- dbt
- Tableau/Looker/Metabase

Data pipeline is largely built with Python, SQLAlchemy, pandas, numpy

### Project architecture


### Data Description
Additionally, an application UK HPI allows users to view statistics . Data is available from 1995 for England and Wales, 2004 for Scotland and 2005 for Northern Ireland. 
