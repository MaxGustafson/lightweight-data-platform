from pathlib import Path

import dlt
from dlt.sources.filesystem import filesystem, read_csv

_BUCKET_URL = f"file://{Path(__file__).resolve().parent.parent.parent / 'input_data'}"


def file_resource_pipeline_csv(
    table: str, domain: str, write_disposition: str = "replace"
) -> None:

    pipeline = dlt.pipeline(
        pipeline_name=f"raw_{domain}_{table}",
        destination=dlt.destinations.duckdb("databases/orders.duckdb"),
        dataset_name=f"{domain}_raw",
    )

    resource = (
        filesystem(bucket_url=_BUCKET_URL, file_glob=f"{table}.csv") | read_csv()
    ).with_name(table)

    info = pipeline.run(resource, write_disposition=write_disposition)
    print(info)
