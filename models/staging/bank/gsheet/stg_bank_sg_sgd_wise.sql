with
source as (
    select *
    from {{ source("google_sheets", "sg_sgd_wise") }}
    where lower(currency) = 'sgd'
),

renamed as (
    select
        'wise-sgd' as bank_source,
        parse_date('%d/%m/%Y', date) as local_date,
        'SGD' as local_currency,
        safe_cast(amount as float64) as local_amount,
        category as category,
        description as description
    from source
)

select *
from renamed
