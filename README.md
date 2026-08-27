## 0. Background

How to run:
1. Cd to repo's root folder
2. uv sync
3. [Setup the DuckDB database] task create-db 
4. task ingest-orders
5. task dbt-build-products 
6. [View the output] duckdb -ui databases/orders.duckdb 

## 1. Data Ingestion

The code for ingestion (files/S3-mock -> duckdb) can be found under ingestion/order_files.py.

For simplicity, a dlt write_disposition of "(full) replace" is used. For a production ready system, we want to keep state using a "merge" or "scd2" write_disposition. Currently we assume full history in files to keep data stateful in the raw layer.

Files currently are not verified against a contract (datatypes, columns etc.). A contract should be established between the producer and the data platform which in turn could form the base of a pydantic model to validate the quality of the files.

The target system is a duckdb local database. It was chosen for its simplicity to set-up for local development but should be replaced by a proper analytics database.

## 2. Data Modelling

I modeled the core data as a star schema. 

The order data are well suited as a fact-metric. We expect a large volumes of orders landing in our platform with few updates to existing orders. The customer and product data are instead enriching information of the metric and better suited as dimensions.

fct_order_items: A denormalized fact-table holding order and order_header information for simple querying. The main drawback of this approach is if order_items ever becomes incremental. Any update in order_header induces an update for all denormalized order_items in the fact-table. An assumption here is that an order doesn't have an absurd amount of order items. Updating a few rows each time an order changes status is feasible.

dim_customer: Descriptive data of the customer. 
dim_product: Descriptive data of the product.

## 3. Data Transformations

ELT in this solution follows these layers:

0_sources (DLT): Stateful, raw data. 1-1 with source.

1_staging (dbt): Cleaning and unifying layer.

2_intermediate (dbt): Optional layer to hold advanced logic (such as joins between staging models).

3_core (dbt): Core layer to serve analytics ready data. Unifying business objects from different sources.

4_products (dbt): Specific data products exposed to consumers. Materialized as tables for efficient querying by consumers.

The requested products are found under transformations/models/4_products/*


## 4. Data Quality
I have added extensive testing throughout the code. Two examples are:

1_staging/stg_customers/customer_id
data_tests:
        - not_null
        - unique

Verifies that the technical identifier from the source exists and is unique within the file. If it fails, our pipeline will be completely wrong as there is no deduplication logic. The pipeline should fail, block downstream materialization and alert the engineering team.

4_products/daily_sales/total_revenue
data_tests:
        - not_null
        - dbt_utils.accepted_range:
        min_value: 0
        inclusive: true
        config:
        severity: warn

Tests that the total revenue has a reasonable value. Failure indicates a logical bug or dirty data. This test should not fail the pipeline as the rest of the model can potentially be consumed (with caution). A clear error should be flagged to the consumer in the dbt generated docs or other shared portal. This should also alert the engineering team.

## 5. Scalability

For the solution to properly scale we can consider multiple approaches. For ingestion, the files should preferably only produce a delta of what was changed since the last run. Alternatively they could be replaced by an api or event stream to allow for incremental consumption. This is especially true for the orders file which has fact like data. 

An orchestrator which allows us to backfill partitions would be useful. A fix to historical data in the source system should not induce a full reload in our platform.

The fact data stored in the raw_layer could be partitioned by date. By also loading the daily_sales product incrementally, we could process only one day of orders at a time, only touching data for that specific date.

Recent data should be stored in a hot partition in e.g. an S3 bucket, while historical data could instead be moved to a cold partition saving storage costs while keeping performance for recent data.

We expect most analytical queries to use the latest value of a dimension (customer + product). If we choose to build a scd2 history, the active version should be kept in a separate partition. We avoid having to sift through historical rows for the most used version. 

