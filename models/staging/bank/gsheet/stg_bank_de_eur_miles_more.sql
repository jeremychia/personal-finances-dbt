with
source as (
    select *
    from {{ source("google_sheets", "de_eur_miles_more") }}
    where processed_on is not null
),

renamed as (
    select
        'miles&more-cc' as bank_source,
        parse_date('%d.%m.%Y', authorised_on) as local_date,
        'EUR' as local_currency,
        safe_cast(
            replace(
                replace(amount, '.', ''), ',', '.'
            ) as float64
        ) as local_amount,  -- convert european format
        category,
        trim(description) as description

    from source
)

select *
from renamed
