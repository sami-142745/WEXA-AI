from arango import ArangoClient
from benchmark.config import *

client = ArangoClient(hosts=ARANGODB_URL)

db = client.db(
    ARANGODB_DATABASE,
    username=ARANGODB_USER,
    password=ARANGODB_PASSWORD,
)

print("\nGraphs:\n")
print(db.graphs())