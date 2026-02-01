with
source as (select * from {{ source("bank", "sg_sgd_revolut_v1") }}),

renamed as (
    select
        'revolut-sgd' as bank_source,
        parse_date('%b %d, %Y', completed_date) as local_date,
        'SGD' as local_currency,
        coalesce(
            safe_cast(paid_in_sgd as float64),
            0
        ) - coalesce(
            safe_cast(paid_out_sgd as float64), 0
        ) as local_amount,
        category2 as category,
        description as description

    from source
)

select *
from renamed
