import argparse

from benchmark.connectors.factory import ConnectorFactory

parser = argparse.ArgumentParser()
parser.add_argument("--db", required=True)

args = parser.parse_args()

db = ConnectorFactory.get(args.db)

db.connect()
db.verify()

print(f"Connected to {args.db}")

# -------------------------
# Database-specific test query
# -------------------------

# -------------------------
# Database-specific test query
# -------------------------

if args.db.lower() == "arangodb":

    result = db.execute("""
    RETURN "Benchmark Ready"
    """)

    print(result[0])

elif args.db.lower() == "age":

    result = db.execute("""
    SELECT 'Benchmark Ready' AS message;
    """)

    print(result[0][0])

else:

    result = db.execute("""
    RETURN 'Benchmark Ready' AS message
    """)

    print(result[0]["message"])