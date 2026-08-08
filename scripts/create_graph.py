from arango import ArangoClient
from benchmark.config import *

client = ArangoClient(hosts=ARANGODB_URL)

db = client.db(
    ARANGODB_DATABASE,
    username=ARANGODB_USER,
    password=ARANGODB_PASSWORD,
)

# Delete old graph if it exists
if db.has_graph("social"):
    db.delete_graph("social")

# Create graph
graph = db.create_graph("social")

graph.create_edge_definition(
    edge_collection="friends",
    from_vertex_collections=["users"],
    to_vertex_collections=["users"],
)

print("Graph created successfully!")