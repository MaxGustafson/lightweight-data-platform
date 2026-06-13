{#
        Assumption:
        Cusotmer_id unique between countries.
#}
with base as (
    select
        customer_id,
        country,
        signup_date,
        {{ orders() }} as source_system
    from {{ source('orders_raw', 'customers') }}
)

select
    customer_id,
    country,
    signup_date,
    source_system,
    {{ generate_guid(['customer_id']) }} as customer_guid
from base
