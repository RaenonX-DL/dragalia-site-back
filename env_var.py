"""Convenient functions to extract information from the environment variables."""
import os

__all__ = ("is_testing",)


def is_testing() -> bool:
    """
    Check if the environment variable ``TEST`` has been set to ``1`` to indicate it's testing.

    :return: if the environment variables indicates it's testing
    """
    return bool(int(os.environ.get("TEST", 0)))
