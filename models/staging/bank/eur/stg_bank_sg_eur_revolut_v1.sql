with
source as (select * from {{ source("bank", "sg_eur_revolut_v1") }}),

renamed as (
    select
        'revolut-eur' as bank_source,
        parse_date('%b %d, %Y', completed_date) as local_date,
        'EUR' as local_currency,
        coalesce(cast(paid_in_eur as float64), 0) - coalesce(
            cast(paid_out_eur as float64), 0
        ) as local_amount,
        category2 as category,
        description as description

    from source
)

select *
from renamed
