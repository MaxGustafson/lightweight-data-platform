{#
        Assumption:
        One customer per order -> UK = {order_id}
#}
with base as (
    select
        order_id,
        customer_id,
        order_timestamp,
        order_status,
        {{ orders() }} as source_system,
        row_number() over (partition by order_id order by order_timestamp desc) as rn
    from {{ source('orders_raw', 'orders') }}
)

select
    {{ generate_guid(['order_id']) }} as order_guid,
    {{ generate_guid(['customer_id']) }} as customer_guid,
    order_id,
    customer_id,
    order_timestamp,
    order_status,
    source_system
from base
where rn = 1
