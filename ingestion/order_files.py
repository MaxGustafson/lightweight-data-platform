"""
Ingestion scripts for the order files.

ASSUMPTIONS:
    Files are placed on fileshare
    They are placed by the same system - so they make sense to group togheter
    Files would probably be exposed via API or placed in an S3 bucket or similar. Kept in repo for simplicity.

TODO:
    Proper orchestration tool instead of if __name__ == __main__
    Dump in local MinIO
    Move processed files to backup/delete processed files

"""

from pathlib import Path

from tools.file_resourses import file_resource_pipeline_csv

_REPO_ROOT: Path = Path(__file__).resolve().parent.parent
_DOMAIN: str = "orders"
_DATABASE_PATH: str = str(_REPO_ROOT / "databases/orders.duckdb")


def dynamic_order_files_resource_factory():

    allow_listed_files: set = {"customers", "order_items", "orders", "products"}

    input_folder: Path = _REPO_ROOT / "input_data"
    errors: list[str] = []

    for csv_file in input_folder.glob("*.csv"):
        try:
            if csv_file.stem not in allow_listed_files:
                raise ValueError(
                    f"Blocked file {csv_file.name} processed for ingestion."
                )
            else:
                file_resource_pipeline_csv(
                    table=csv_file.stem,
                    domain=_DOMAIN,
                    trg_destination_path=_DATABASE_PATH,
                    src_filesystem_path=input_folder,
                )

        except ValueError as e:
            errors.append(str(e))

    # Error handling
    if errors:
        raise RuntimeError(
            f"{len(errors)} file(s) could not be processed:\n"
            + "\n".join(f"- {error}" for error in errors)
            + f"\nThe following file-stems are allowed : {[stem + '.csv' for stem in allow_listed_files]}. "
        )


if __name__ == "__main__":
    dynamic_order_files_resource_factory()
