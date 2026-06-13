{#
        Generates a surrogate key (guid) from source_system plus the provided columns.
        Wraps dbt_utils.generate_surrogate_key so source_system is always part of the key.
#}
{% macro generate_guid(columns) -%}
    {{ dbt_utils.generate_surrogate_key(['source_system'] + columns) }}
{%- endmacro %}
