with
source as (
    select *
    from {{ source("google_sheets", "gb_gbp_wise") }}
    where lower(currency) = 'gbp'
),

renamed as (
    select
        'wise-gbp' as bank_source,
        parse_date('%d-%m-%Y', date) as local_date,
        'GBP' as local_currency,
        safe_cast(amount as float64) as local_amount,
        category as category,
        description as description

    from source
)

select *
from renamed
