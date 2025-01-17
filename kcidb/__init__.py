"""Kernel CI database management"""

import argparse
import json
import sys
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
from kcidb import db_schema
from kcidb import io_schema


class Client:
    """Kernel CI database client"""

    def __init__(self, dataset_name):
        """
        Initialize a Kernel CI database client.

        Args:
            dataset_name:   The name of the Kernel CI dataset. The dataset
                            should be located within the Google Cloud project
                            specified in the credentials file pointed to by
                            GOOGLE_APPLICATION_CREDENTIALS environment
                            variable.
        """
        assert isinstance(dataset_name, str)
        self.client = bigquery.Client()
        self.dataset_ref = self.client.dataset(dataset_name)

    def init(self):
        """
        Initialize the database. The database must be empty.
        """
        for table_name, table_schema in db_schema.TABLE_MAP.items():
            table_ref = self.dataset_ref.table(table_name)
            table = bigquery.table.Table(table_ref, schema=table_schema)
            self.client.create_table(table)

    def cleanup(self):
        """
        Cleanup (empty) the database, removing all data.
        """
        for table_name, _ in db_schema.TABLE_MAP.items():
            table_ref = self.dataset_ref.table(table_name)
            self.client.delete_table(table_ref)

    def query(self):
        """
        Query data from the database.

        Returns:
            The JSON data from the database adhering to the I/O schema
            (kcidb.io_schema.JSON).
        """
        data = dict(version="1")
        for obj_list_name in db_schema.TABLE_MAP:
            job_config = bigquery.job.QueryJobConfig(
                default_dataset=self.dataset_ref)
            query_job = self.client.query(
                f"SELECT * FROM `{obj_list_name}`", job_config=job_config)
            obj_list = []
            for row in query_job:
                obj = dict(item for item in row.items() if item[1] is not None)
                # Parse the "misc" fields
                if "misc" in obj:
                    obj["misc"] = json.loads(obj["misc"])
                obj_list.append(obj)
            data[obj_list_name] = obj_list
        io_schema.validate(data)
        return data

    def submit(self, data):
        """
        Submit data to the database.

        Args:
            data:   The JSON data to submit to the database.
                    Must adhere to the I/O schema (kcidb.io_schema.JSON).
        """
        io_schema.validate(data)
        for obj_list_name in db_schema.TABLE_MAP:
            if obj_list_name in data:
                obj_list = data[obj_list_name]
                # Flatten the "misc" fields
                for obj in obj_list:
                    if "misc" in obj:
                        obj["misc"] = json.dumps(obj["misc"])
                # Store
                job_config = bigquery.job.LoadJobConfig(
                    autodetect=False,
                    schema=db_schema.TABLE_MAP[obj_list_name])
                job = self.client.load_table_from_json(
                    obj_list,
                    self.dataset_ref.table(obj_list_name),
                    job_config=job_config)
                try:
                    job.result()
                except BadRequest:
                    raise Exception("".join([
                        f"ERROR: {error['message']}\n" for error in job.errors
                    ]))


def query_main():
    """Execute the kcidb-query command-line tool"""
    description = 'kcidb-query - Query test results from kernelci.org database'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-d', '--dataset',
        help='Dataset name',
        required=True
    )
    args = parser.parse_args()
    client = Client(args.dataset)
    json.dump(client.query(), sys.stdout, indent=4, sort_keys=True)


def submit_main():
    """Execute the kcidb-submit command-line tool"""
    description = 'kcidb-submit - Submit test results to kernelci.org database'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-d', '--dataset',
        help='Dataset name',
        required=True
    )
    args = parser.parse_args()
    data = json.load(sys.stdin)
    io_schema.validate(data)
    client = Client(args.dataset)
    client.submit(data)


def init_main():
    """Execute the kcidb-init command-line tool"""
    description = 'kcidb-init - Initialize a kernelci.org database'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-d', '--dataset',
        help='Dataset name',
        required=True
    )
    args = parser.parse_args()
    client = Client(args.dataset)
    client.init()


def cleanup_main():
    """Execute the kcidb-cleanup command-line tool"""
    description = 'kcidb-cleanup - Cleanup a kernelci.org database'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-d', '--dataset',
        help='Dataset name',
        required=True
    )
    args = parser.parse_args()
    client = Client(args.dataset)
    client.cleanup()


def schema_main():
    """Execute the kcidb-schema command-line tool"""
    description = 'kcidb-schema - Output I/O JSON schema'
    parser = argparse.ArgumentParser(description=description)
    parser.parse_args()
    json.dump(io_schema.JSON, sys.stdout, indent=4, sort_keys=True)
