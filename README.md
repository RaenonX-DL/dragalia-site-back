# dragalia-posts-site-back

Backend of the dragalia posts site.

# Environment Variables

Name | Required/Optional | Description
:---: | :---: | :---:
MONGO_URL | Required | Connection string of MongoDB database.
MONGO_DB | Optional | Database to use. If specified, all data will be manipulated in the given database only.
TEST | Optional | Specify this to `1` for CI test-specific behavior.
