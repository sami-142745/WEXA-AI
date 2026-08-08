from benchmark.connectors.memgraph import MemgraphConnector

db = MemgraphConnector()

db.connect()
db.verify()

print("✅ Connected to Memgraph!")

result = db.execute("RETURN 'Hello Memgraph' AS message")

print(result[0]["message"])

db.close()