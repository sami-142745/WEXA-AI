import gzip
from pathlib import Path

import psycopg2

from benchmark.config import (
    AGE_HOST,
    AGE_PORT,
    AGE_DATABASE,
    AGE_USER,
    AGE_PASSWORD,
)

GRAPH = "cognodb"

BATCH_SIZE = 1000
MAX_RELATIONSHIPS = 100000


def main():

    conn = psycopg2.connect(
        host=AGE_HOST,
        port=AGE_PORT,
        database=AGE_DATABASE,
        user=AGE_USER,
        password=AGE_PASSWORD,
    )

    cur = conn.cursor()

    cur.execute("LOAD 'age';")
    cur.execute('SET search_path = ag_catalog, "$user", public;')

    # Create graph if it doesn't exist
    try:
        cur.execute(f"SELECT create_graph('{GRAPH}');")
        conn.commit()
    except Exception:
        conn.rollback()

    dataset = Path("datasets/soc-pokec-relationships.txt.gz")

    count = 0

    with gzip.open(dataset, "rt", encoding="utf-8") as f:

        for line in f:

            if line.startswith("#"):
                continue

            src, dst = line.strip().split()

            query = f"""
            SELECT *
            FROM cypher('{GRAPH}', $$
                MERGE (a:User {{id:{int(src)}}})
                MERGE (b:User {{id:{int(dst)}}})
                MERGE (a)-[:FRIEND]->(b)
            $$) AS (v agtype);
            """

            cur.execute(query)

            count += 1

            if count % BATCH_SIZE == 0:
                conn.commit()
                print(f"Imported {count:,}")

            if count >= MAX_RELATIONSHIPS:
                break

    conn.commit()

    cur.close()
    conn.close()

    print(f"\nFinished importing {count:,} relationships")


if __name__ == "__main__":
    main()