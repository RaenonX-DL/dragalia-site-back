"""Various configs related to the database and the connection to it."""
import os
import time

from pymongo import MongoClient

from env_var import is_testing

__all__ = ("MONGO_URL", "MONGO_CLIENT", "get_single_db_name", "SINGLE_DB_NAME", "is_test_db",)

MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
    print("Specify connection string to MongoDB instance as `MONGO_URL` in environment variable.")
    exit(1)

MONGO_CLIENT = MongoClient(MONGO_URL)


def get_single_db_name():
    """
    Get the single db name, if any.

    Should only being called in the tests or when the module is initialized.
    """
    expected_db_name = os.environ.get("MONGO_DB")
    if not expected_db_name and is_testing():
        expected_db_name = f"Test-{time.time_ns() // 1000000}"

    return expected_db_name


SINGLE_DB_NAME = get_single_db_name()
if is_testing():
    print("MongoDB single database activated because `TEST` has been set to true.")
    print(f"MongoDB single database name: {SINGLE_DB_NAME}")
elif SINGLE_DB_NAME:
    print("MongoDB single database is activated "
          "by setting values to the environment variable 'MONGO_DB'.")
    print(f"MongoDB single database name: {SINGLE_DB_NAME}")


def is_test_db(db_name: str):
    """Check if ``db_name`` is a test database."""
    if "-" in db_name:
        prefix, epoch = db_name.split("-", 2)

        # Consider the database created 10 mins before this call as the test database
        return "Test" in prefix and int(epoch) < time.time_ns() // 1000000 - 600000

    return False
