with
source as (select * from {{ source("google_sheets", "sg_sgd_uob") }}),

renamed as (
    select
        'uob' as bank_source,
        parse_date(
            '%d-%b-%y', transaction_date
        ) as local_date,
        'SGD' as local_currency,
        coalesce(
            safe_cast(deposit as float64),
            0
        ) - coalesce(
            safe_cast(withdrawal as float64), 0
        ) as local_amount,
        category,
        transaction_description as description
    from source
)

select *
from renamed
