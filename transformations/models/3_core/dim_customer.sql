select
    customer_guid,
    customer_id,
    country,
    signup_date,
    source_system
from {{ ref('stg_customers') }}
