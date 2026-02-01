with
source as (select * from {{ source("google_sheets", "sg_sgd_revolut_v2") }}),

renamed as (
    select
        'revolut-sgd' as bank_source,
        date(
            parse_datetime('%d/%m/%Y %H:%M', started_date)
        ) as local_date,
        'SGD' as local_currency,
        safe_cast(amount as float64) as local_amount,
        category as category,
        description as description
    from source
)

select *
from renamed
