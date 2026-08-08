from benchmark.connectors.factory import ConnectorFactory
from benchmark.benchmark_runner import BenchmarkRunner

DATABASES = [
    "cognodb",
    "neo4j",
    "memgraph",
]

QUERY = """
MATCH (n)
RETURN count(n) AS total
"""


for db_name in DATABASES:

    print("\n" + "=" * 60)
    print(db_name.upper())
    print("=" * 60)

    db = ConnectorFactory.get(db_name)

    db.connect()

    db.verify()

    runner = BenchmarkRunner()

    result = runner.run(
        lambda: db.execute(QUERY)
    )

    print(f"Average : {result['Average']} ms")
    print(f"P50     : {result['P50']} ms")
    print(f"P95     : {result['P95']} ms")

    db.close()