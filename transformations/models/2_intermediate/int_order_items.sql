{#
    Grain: one row per order line (order_id x product_id) under a given source_system.
    Header attributes (order_timestamp, order_status) denormalized down onto the line.
#}
with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
)

select
    oi.order_item_guid,
    oi.order_guid,
    o.customer_guid,
    oi.product_guid,
    oi.order_id,
    oi.product_id,
    o.customer_id,
    o.order_timestamp,
    o.order_status,
    oi.quantity,
    oi.price_per_unit,
    oi.source_system,
    oi.quantity * oi.price_per_unit as line_amount
from order_items as oi
inner join orders as o
    on oi.order_guid = o.order_guid
