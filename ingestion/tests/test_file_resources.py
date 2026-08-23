from dataclasses import dataclass
from pathlib import Path

import pytest
from tools.file_resourses import file_resource_pipeline_csv


@dataclass
class TestEnvironment:
    src_input_dir: Path
    src_csv_file: Path
    trg_database_path: Path


@pytest.fixture
def test_environment(tmp_path):

    input_dir: Path = tmp_path / "input_data"
    input_dir.mkdir()

    csv_file: Path = input_dir / "customers.csv"
    csv_file.write_text("customer_id,name\n1,Alice\n2,Bob\n")

    database_path: Path = tmp_path / "orders.duckdb"

    return TestEnvironment(input_dir, csv_file, database_path)


def test_file_resource_pipeline_csv(test_environment: TestEnvironment):

    file_resource_pipeline_csv(
        table="customers",
        domain="orders",
        trg_destination_path=str(test_environment.trg_database_path),
        src_filesystem_path=str(test_environment.src_input_dir),
    )
