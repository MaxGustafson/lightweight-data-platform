select
    order_item_guid,
    order_guid,
    customer_guid,
    product_guid,
    order_id,
    product_id,
    customer_id,
    order_timestamp,
    order_status,
    quantity,
    price_per_unit,
    source_system,
    line_amount
from {{ ref('int_order_items') }}
