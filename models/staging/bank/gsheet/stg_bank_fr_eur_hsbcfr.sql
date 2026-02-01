with
source as (select * from {{ source("google_sheets", "fr_eur_hsbcfr") }}),

renamed as (
    select
        'hsbc-fr' as bank_source,
        parse_date('%d/%m/%Y', operation) as local_date,
        'EUR' as local_currency,
        coalesce(
            cast(
                replace(
                    replace(credit, ',', '.'), ' ', ''
                ) as float64
            ),
            0
        ) + coalesce(
            cast(
                replace(
                    replace(debit, ',', '.'), ' ', ''
                ) as float64
            ),
            0
        ) as local_amount,
        category as category,
        description as description

    from source
)

select *
from renamed
