{{ config(materialized='view') }}

select 
-- date
cast(Date as timestamp) as dates,

-- identifier
cast(region_name as string) as region_name,
cast(area_code as string) as area_code,

-- cash dimensions
cast(cash_average_price as numeric) as cash_average_price,
cast(cash_index as numeric) as cash_index,
cast(cash_monthly_change as numeric) as cash_monthly_change,
cast(cash_annual_change as numeric) as cash_annual_change,
cast(cash_sales_volume as numeric) as cash_sales_volume,

-- mortgage dimensions
cast(mortgage_average_price as numeric) as mortgage_average_price,
cast(mortgage_index as numeric) as mortgage_index,
cast(mortgage_monthly_change as numeric) as mortgage_monthly_change,
cast(mortgage_annual_change as numeric) as mortgage_annual_change,
cast(mortgage_sales_volume as numeric) as mortgage_sales_volume,

 from {{ source('staging' ,'cash-mortgage-sales') }}
limit 100