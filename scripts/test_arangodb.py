from arango import ArangoClient
from benchmark.config import (
    ARANGODB_URL,
    ARANGODB_DATABASE,
    ARANGODB_USER,
    ARANGODB_PASSWORD,
)

print("URL:", ARANGODB_URL)
print("Database:", ARANGODB_DATABASE)
print("User:", ARANGODB_USER)

client = ArangoClient(hosts=ARANGODB_URL)

db = client.db(
    ARANGODB_DATABASE,
    username=ARANGODB_USER,
    password=ARANGODB_PASSWORD,
)

print(db.version())