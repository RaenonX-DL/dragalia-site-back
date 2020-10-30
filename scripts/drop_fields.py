"""Script to drop the fields."""
from controllers.base import MONGO_CLIENT

NAME_DB = "post"
NAME_COL = "quest"

DT_PUBLISHED: str = "_dt_pub"
DT_LAST_MODIFIED: str = "_dt_mod"

MODIFY_NOTES: str = "_dt_mn"
MODIFY_DT: str = "_ts"
MODIFY_NOTE: str = "_n"

DROP_FIELDS: list[str] = []


# The key and the value of ``COPY_VAL`` means the key of the source and the destination.


def main():
    col = MONGO_CLIENT.get_database(NAME_DB).get_collection(NAME_COL)

    update_result = col.update_many(
        {},
        {"$unset": DROP_FIELDS}
    )

    print(f"Updating the collection `{NAME_DB}.{NAME_COL}`...")
    print(f"{update_result.matched_count} records matches the update criteria.")
    print(f"{update_result.modified_count} records was updated.")


if __name__ == '__main__':
    main()
