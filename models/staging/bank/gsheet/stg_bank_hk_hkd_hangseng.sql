with
source as (select * from {{ source("google_sheets", "hk_hkd_hangseng") }}),

renamed as (
    select
        'hangseng' as bank_source,
        parse_date('%d/%m/%Y', date_ddmmyyyy) as local_date,
        'HKD' as local_currency,
        coalesce(safe_cast(credit as float64), 0) - coalesce(
            safe_cast(debit as float64), 0
        ) as local_amount,
        category as category,
        details as description

    from source
)

select *
from renamed
