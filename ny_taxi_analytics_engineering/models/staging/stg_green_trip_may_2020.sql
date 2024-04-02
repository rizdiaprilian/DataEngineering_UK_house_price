with tripdata_source as (

    select *,
        row_number() over(partition by vendorid, lpep_pickup) as rn
    from {{ source('staging', 'green_trip_may_2020') }}
    where vendorid is not null

)

    select
    --- identifiers
        {{ dbt_utils.generate_surrogate_key(['vendorid', 'lpep_pickup']) }} as trip_id,
        {{ dbt.safe_cast("vendorid", api.Column.translate_type("integer")) }} as vendorid,
        {{ dbt.safe_cast("ratecodeid", api.Column.translate_type("integer")) }} as ratecodeid,
        {{ dbt.safe_cast("pulocationid", api.Column.translate_type("integer")) }} as pickup_locationid,
        {{ dbt.safe_cast("dolocationid", api.Column.translate_type("integer")) }} as dropoff_locationid,
    --- timestamps
        cast(lpep_pickup as timestamp) as pickup_datetime,
        cast(lpep_dropoff as timestamp) as dropoff_datetime,
        
    --- trip info
        store_and_fwd_flag,
        {{ dbt.safe_cast("passenger_count", api.Column.translate_type("integer")) }} as passenger_count,
        cast(trip_distance as numeric) as trip_distance,
        {{ dbt.safe_cast("trip_type", api.Column.translate_type("integer")) }} as trip_type,

    --- payment info
        cast(fare_amount as numeric) as fare_amount,
        cast(extra as numeric) as extra,
        cast(mta_tax as numeric) as mta_tax,
        cast(tip_amount as numeric) as tip_amount,
        cast(tolls_amount as numeric) as tolls_amount,
        cast(ehail_fee as numeric) as ehail_fee,
        cast(improvement_surcharge as numeric) as improvement_surcharge,
        cast(congestion_surcharge as numeric) as congestion_surcharge,
        cast(total_amount as numeric) as total_amount,
        coalesce({{ dbt.safe_cast("payment_type", api.Column.translate_type("integer")) }},0) as payment_type,
        {{ get_payment_type_description("payment_type") }} as payment_type_description
        

    from tripdata_source
    where rn = 1

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}

