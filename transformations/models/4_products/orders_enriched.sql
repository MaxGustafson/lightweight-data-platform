with orders_aggregated as (

    select
        order_id,
        any_value(customer_guid) as customer_guid,
        any_value(order_timestamp) as order_timestamp,
        any_value(customer_id) as customer_id,
        sum(line_amount) as order_total_amount,
        sum(quantity) as number_of_items
    from {{ ref('fct_order_items') }}
    group by order_id
),

cte as (
    select
        fct.order_id,
        fct.order_timestamp,
        fct.customer_id,
        cust.country,
        fct.order_total_amount,
        fct.number_of_items
    from orders_aggregated as fct
    left join {{ ref('dim_customer') }} as cust on fct.customer_guid = cust.customer_guid
)

select
    order_id,
    order_timestamp,
    customer_id,
    country,
    order_total_amount,
    number_of_items
from cte
