{{ config(
    materialized = "table",
    tags = ["staging", "invm"]
) }}

with
source as (select * from {{ source("google_sheets", "sgd_invm") }}),

renamed as (
    select
        parse_date('%d/%m/%Y', date) as local_date,
        'SGD' as local_currency_market,
        safe_cast(market_sgd as float64) as local_market,
        safe_cast(base_sgd as float64) as sgd_base,
        investment as investment_source,
        safe_cast(is_redeemed as boolean) as is_redeemed

    from source
)

select *
from renamed
where local_date is not null
