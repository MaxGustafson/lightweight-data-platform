{% docs customers__table %}
Customer master data.
{% enddocs %}

{% docs customers__customer_id %}
Primary key for a customer.
{% enddocs %}

{% docs customers__country %}
ISO country of the customer.
{% enddocs %}

{% docs customers__signup_date %}
Date the customer signed up (string from source).
{% enddocs %}

{% docs orders__table %}
One row per order.
{% enddocs %}

{% docs orders__order_id %}
Primary key for an order.
{% enddocs %}

{% docs orders__customer_id %}
FK to customers.customer_id.
{% enddocs %}

{% docs orders__order_timestamp %}
Timestamp (with timezone) when the order was placed.
{% enddocs %}

{% docs orders__order_status %}
Lifecycle status of the order.
{% enddocs %}

{% docs order_items__table %}
Line items belonging to each order.
{% enddocs %}

{% docs order_items__order_id %}
FK to orders.order_id.
{% enddocs %}

{% docs order_items__product_id %}
FK to products.product_id.
{% enddocs %}

{% docs order_items__quantity %}
Units of the product on this line.
{% enddocs %}

{% docs order_items__price_per_unit %}
Price charged per unit on this line.
{% enddocs %}

{% docs products__table %}
Product catalog.
{% enddocs %}

{% docs products__product_id %}
Primary key for a product.
{% enddocs %}

{% docs products__category %}
Product category.
{% enddocs %}

{% docs products__product_name %}
Human-readable product name.
{% enddocs %}
