from benchmark.connectors.cognodb import CognoDBConnector

db = CognoDBConnector()
db.connect()
db.verify()

nodes = db.execute("""
MATCH (n:User)
RETURN count(n) AS count
""")[0]["count"]

relationships = db.execute("""
MATCH ()-[r:FRIEND]->()
RETURN count(r) AS count
""")[0]["count"]

print("=" * 40)
print("DATASET SUMMARY")
print("=" * 40)
print(f"Nodes         : {nodes:,}")
print(f"Relationships : {relationships:,}")

db.close()