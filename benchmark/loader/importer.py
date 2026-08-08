import gzip
import time
from pathlib import Path

from benchmark.connectors.cognodb import CognoDBConnector

BATCH_SIZE = 10000
MAX_RELATIONSHIPS = 100000


class DatasetImporter:

    def __init__(self):
        self.db = CognoDBConnector()

    def import_dataset(self):

        start_time = time.time()

        self.db.connect()
        self.db.verify()

        print("Clearing database...")
        self.db.execute("MATCH (n) DETACH DELETE n")

        print("Creating index...")
        try:
            self.db.execute("""
            CREATE INDEX user_id IF NOT EXISTS
            FOR (u:User)
            ON (u.id)
            """)
        except Exception as e:
            print(f"Index creation skipped: {e}")

        dataset = Path("datasets/soc-pokec-relationships.txt.gz")

        if not dataset.exists():
            raise FileNotFoundError(f"{dataset} not found.")

        relationships = []
        users = set()
        count = 0

        print(f"Reading first {MAX_RELATIONSHIPS:,} relationships...")

        with gzip.open(dataset, "rt", encoding="utf-8") as f:

            for line in f:

                if line.startswith("#"):
                    continue

                src, dst = line.strip().split()

                src = int(src)
                dst = int(dst)

                users.add(src)
                users.add(dst)

                relationships.append({
                    "src": src,
                    "dst": dst
                })

                count += 1

                if count >= MAX_RELATIONSHIPS:
                    break

        print(f"Unique Users: {len(users):,}")
        print(f"Relationships: {len(relationships):,}")

        # ---------------------------------
        # Phase 1 - Create User Nodes
        # ---------------------------------

        print("\nCreating users...")

        user_list = list(users)

        for i in range(0, len(user_list), BATCH_SIZE):

            batch = user_list[i:i + BATCH_SIZE]

            self.db.execute("""
            UNWIND $users AS id
            MERGE (:User {id:id})
            """, {"users": batch})

            print(
                f"Users: "
                f"{min(i + BATCH_SIZE, len(user_list)):,}"
                f"/{len(user_list):,}"
            )

        # ---------------------------------
        # Phase 2 - Create Relationships
        # ---------------------------------

        print("\nCreating relationships...")

        for i in range(0, len(relationships), BATCH_SIZE):

            batch = relationships[i:i + BATCH_SIZE]

            self.db.execute("""
            UNWIND $rows AS row

            MATCH (a:User {id: row.src})
            MATCH (b:User {id: row.dst})

            CREATE (a)-[:FRIEND]->(b)
            """, {"rows": batch})

            print(
                f"Relationships: "
                f"{min(i + BATCH_SIZE, len(relationships)):,}"
                f"/{len(relationships):,}"
            )

        elapsed = time.time() - start_time

        self.db.close()

        print("\n✅ Import completed successfully!")
        print(f"Users Created            : {len(users):,}")
        print(f"Relationships Imported   : {count:,}")
        print(f"Load Time                : {elapsed:.2f} seconds")
        print(f"Relationships/sec        : {count / elapsed:.2f}")