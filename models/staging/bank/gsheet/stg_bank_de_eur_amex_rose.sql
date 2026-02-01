with
source as (select * from {{ source("google_sheets", "de_eur_amex_rose") }}),

renamed as (
    select
        'amex_rose-cc' as bank_source,
        parse_date('%d/%m/%Y', datum) as local_date,
        'EUR' as local_currency,
        -safe_cast(
            replace(betrag, ',', '.') as float64
        ) as local_amount,
        category as category,
        beschreibung as description
    from source
)

select *
from renamed
