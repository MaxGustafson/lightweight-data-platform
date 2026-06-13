{#
        Assumption:
        UK = {product_id}
#}
with base as (
    select
        product_id,
        category,
        product_name,
        {{ orders() }} as source_system
    from {{ source('orders_raw', 'products') }}
)

select
    {{ generate_guid(['product_id']) }} as product_guid,
    product_id,
    category,
    product_name,
    source_system
from base
