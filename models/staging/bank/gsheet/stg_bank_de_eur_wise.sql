with
source as (
    select *
    from {{ source("google_sheets", "de_eur_wise") }}
    where lower(currency) = 'eur'
),

renamed as (
    select
        'wise-eur' as bank_source,
        parse_date('%d-%m-%Y', date) as local_date,
        'EUR' as local_currency,
        safe_cast(amount as float64) as local_amount,
        category as category,
        description as description

    from source
)

select *
from renamed
