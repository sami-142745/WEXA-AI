import gzip
from pathlib import Path

from benchmark.connectors.neo4j import Neo4jConnector

BATCH_SIZE = 1000
MAX_RELATIONSHIPS = 100000


def insert_batch(db, rows):
    query = """
    UNWIND $rows AS row

    MERGE (a:User {id: row.src})
    MERGE (b:User {id: row.dst})

    MERGE (a)-[:FRIEND]->(b)
    """

    db.execute(query, {"rows": rows})


def main():

    db = Neo4jConnector()

    db.connect()
    db.verify()

    print("Connected to Neo4j")

    print("Clearing database...")
    db.execute("MATCH (n) DETACH DELETE n")

    dataset = Path("datasets/soc-pokec-relationships.txt.gz")

    batch = []
    count = 0

    with gzip.open(dataset, "rt", encoding="utf-8") as f:

        for line in f:

            if line.startswith("#"):
                continue

            src, dst = line.strip().split()

            batch.append({
                "src": int(src),
                "dst": int(dst),
            })

            count += 1

            if len(batch) >= BATCH_SIZE:
                insert_batch(db, batch)
                batch.clear()

                if count % 10000 == 0:
                    print(f"Imported {count:,}")

            if count >= MAX_RELATIONSHIPS:
                break

    if batch:
        insert_batch(db, batch)

    db.close()

    print(f"\nFinished importing {count:,} relationships")


if __name__ == "__main__":
    main()