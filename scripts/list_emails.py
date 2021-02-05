from controllers.base import MONGO_CLIENT


def main():
    col = MONGO_CLIENT.get_database("user").get_collection("google")

    print(f"Emails #: {col.estimated_document_count()}")

    contacts = ["E-mail Address\n"]
    for entry in col.find():
        contacts.append(f"{entry['em']}\n")

    with open("contacts.csv", "w") as f:
        f.writelines(contacts)


if __name__ == '__main__':
    main()
