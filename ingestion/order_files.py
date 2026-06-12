"""
Ingestion scripts for the order files.

ASSUMPTIONS:
    Files are placed on fileshare
    They are placed by the same system - so they make sense to group togheter
    Files would probably be exposed via API or placed in an S3 bucket or similar. Kept in repo for simplicity.

TODO:
    Proper orchestration tool instead of if __name__ == __main__
    Incremental load
    Dump in local MinIO

"""

from tools.file_resourses import file_resource_pipeline_csv

_DOMAIN: str = "orders"


def customers() -> None:
    file_resource_pipeline_csv(table="customers", domain=_DOMAIN)


def orders() -> None:
    file_resource_pipeline_csv(table="orders", domain=_DOMAIN)


def order_items() -> None:
    file_resource_pipeline_csv(table="order_items", domain=_DOMAIN)


def products() -> None:
    file_resource_pipeline_csv(table="products", domain=_DOMAIN)


if __name__ == "__main__":
    customers()
    orders()
    order_items()
    products()
