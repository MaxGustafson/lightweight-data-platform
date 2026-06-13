{#
        Assumption:
        Grain is one row per (order_id, product_id) line item.
#}
with base as (
    select
        order_id,
        product_id,
        quantity,
        price_per_unit,
        {{ orders() }} as source_system
    from {{ source('orders_raw', 'order_items') }}
)

select
    {{ generate_guid(['order_id', 'product_id']) }} as order_item_guid,
    {{ generate_guid(['order_id']) }} as order_guid,
    {{ generate_guid(['product_id']) }} as product_guid,
    order_id,
    product_id,
    quantity,
    price_per_unit,
    source_system
from base
