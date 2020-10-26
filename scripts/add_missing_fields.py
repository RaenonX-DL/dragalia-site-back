"""Script to add missing fields."""
from controllers.base import MONGO_CLIENT


NAME_DB = "post"
NAME_COL = "quest"


UPDATE_VAL = {
    "c": 0
}


# Only the records that do not have ALL of the fields in `UPDATE_VAL` will be updated.
# i.e. If the record has any of the field in `UPDATE_VAL`, then it will not be updated.


def main():
    col = MONGO_CLIENT.get_database(NAME_DB).get_collection(NAME_COL)

    update_result = col.update_many(
        {update_key: {"$exists": False} for update_key in UPDATE_VAL},
        {"$set": UPDATE_VAL}
    )

    print(f"Updating the collection `{NAME_DB}.{NAME_COL}`...")
    print(f"{update_result.matched_count} records matches the update criteria.")
    print(f"{update_result.modified_count} records was updated.")


if __name__ == '__main__':
    main()
