"""Script to copy the fields from one to another with the same value but different key."""
from controllers.base import MONGO_CLIENT

NAME_DB = "post"
NAME_COL = "analysis"

COPY_KEY: dict[str, str] = {
    "s": "_seq",
    "l": "_lang",
    "d_p": "_dt_pub",
    "d_m": "_dt_mod",
    "m_n": "_dt_mn",
    "c": "_vc"
}


# The key and the value of ``COPY_KEY`` means the key of the source and the destination.


def main():
    col = MONGO_CLIENT.get_database(NAME_DB).get_collection(NAME_COL)

    update_result = col.update_many(
        {},
        [{"$set": {dst: f"${src}" for src, dst in COPY_KEY.items()}}]
    )

    print(f"Updating the collection `{NAME_DB}.{NAME_COL}`...")
    print(f"{update_result.matched_count} records matches the update criteria.")
    print(f"{update_result.modified_count} records was updated.")


if __name__ == '__main__':
    main()
