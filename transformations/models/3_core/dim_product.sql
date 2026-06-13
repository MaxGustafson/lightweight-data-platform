select
    product_guid,
    product_id,
    category,
    product_name,
    source_system
from {{ ref('stg_products') }}
