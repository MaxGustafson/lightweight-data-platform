with orders_aggregated as (

    select
        order_id,
        any_value(order_timestamp) as order_timestamp,
        sum(line_amount) as order_total_amount
    from {{ ref('fct_order_items') }}
    where order_status = 'completed' --Only include orders which provide revenue
    group by order_id
),

date_aggregation as (
    select
        cast(order_timestamp as date) as order_date,
        sum(order_total_amount) as total_revenue,
        count(order_id) as total_orders,
        avg(order_total_amount) as average_order_value
    from orders_aggregated
    group by cast(order_timestamp as date)
)

select
    order_date,
    total_revenue,
    total_orders,
    average_order_value
from date_aggregation
