with base as (
    select
        prod.category,
        sum(fct.line_amount) as total_revenue,
        sum(fct.quantity) as total_quantity_sold
    from {{ ref('fct_order_items') }} as fct
    left join {{ ref('dim_product') }} as prod on fct.product_guid = prod.product_guid
    group by prod.category
)

select
    category,
    total_revenue,
    total_quantity_sold
from base
