with green_trip_2020 as (
    select *
    from {{ ref('stg_green_trip_january_2020') }}
    union all
    select *
    from {{ ref('stg_green_trip_february_2020') }}
    union all
    select *
    from {{ ref('stg_green_trip_march_2020') }}
    union all
    select *
    from {{ ref('stg_green_trip_april_2020') }}
    union all
    select *
    from {{ ref('stg_green_trip_may_2020') }}
    union all
    select *
    from {{ ref('stg_green_trip_june_2020') }}
)
    select * from green_trip_2020