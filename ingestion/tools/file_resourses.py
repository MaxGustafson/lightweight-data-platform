from datetime import UTC, datetime
from pathlib import Path

import dlt
from dlt.sources.filesystem import filesystem, read_csv


def _add_insert_time(row: dict) -> dict:
    row["insert_time"] = datetime.now(UTC)
    return row


def _add_file_name(row: dict, *, file_name: str):
    row["source_file_name"] = file_name
    return row


def file_resource_pipeline_csv(
    table: str,
    domain: str,
    trg_destination_path: str,
    src_filesystem_path: str,
    write_disposition: str = "replace",
) -> None:

    pipeline = dlt.pipeline(
        pipeline_name=f"raw_{domain}_{table}",
        destination=dlt.destinations.duckdb(trg_destination_path),
        dataset_name=f"{domain}_raw",
    )

    bucket_url = f"file://{Path(src_filesystem_path).resolve()}"

    resource = (
        (filesystem(bucket_url=bucket_url, file_glob=f"{table}.csv") | read_csv())
        .with_name(table)
        .add_map(_add_insert_time)
        .add_map(lambda row: _add_file_name(row, file_name=f"{table}.csv"))
    )

    info = pipeline.run(resource, write_disposition=write_disposition)
    print(info)
