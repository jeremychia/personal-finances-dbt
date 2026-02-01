{{ config(
    materialized = "table",
    tags = ["staging", "invm"]
) }}

with
source as (select * from {{ source("google_sheets", "usd_invm") }}),

renamed as (
    select
        parse_date('%d/%m/%Y', date) as local_date,
        'USD' as local_currency_market,
        safe_cast(market_usd as float64) as local_market,
        safe_cast(base_usd as float64) as usd_base,
        safe_cast(base_sgd as float64) as sgd_base,
        investment as investment_source

    from source
)

select *
from renamed
