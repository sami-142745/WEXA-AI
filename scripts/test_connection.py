from benchmark.connectors.cognodb import CognoDBConnector


db = CognoDBConnector()

db.connect()

db.verify()

print("Connected Successfully")

result = db.execute(
    """
    RETURN 'Hello CognoDB' AS message
    """
)

print(result[0]["message"])

db.close()