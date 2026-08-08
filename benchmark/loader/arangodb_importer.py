import gzip
from pathlib import Path

from arango import ArangoClient

from benchmark.config import (
    ARANGODB_URL,
    ARANGODB_DATABASE,
    ARANGODB_USER,
    ARANGODB_PASSWORD,
)

BATCH_SIZE = 1000
MAX_RELATIONSHIPS = 100000


class ArangoImporter:

    def __init__(self):

        self.client = ArangoClient(hosts=ARANGODB_URL)

        self.db = self.client.db(
            ARANGODB_DATABASE,
            username=ARANGODB_USER,
            password=ARANGODB_PASSWORD,
        )

        self.users = None
        self.friends = None

    def setup(self):

        print("Preparing collections...")

        collections = [c["name"] for c in self.db.collections()]

        if "friends" in collections:
            self.db.delete_collection("friends")

        if "users" in collections:
            self.db.delete_collection("users")

        self.users = self.db.create_collection("users")

        self.friends = self.db.create_collection(
            "friends",
            edge=True,
        )

        print("Collections created successfully.")

    def flush(self, users, edges):

        if users:
            self.users.import_bulk(
                list(users.values()),
                on_duplicate="ignore",
            )

        if edges:
            self.friends.import_bulk(edges)

    def import_dataset(self):

        self.setup()

        dataset = Path("datasets/soc-pokec-relationships.txt.gz")

        if not dataset.exists():
            raise FileNotFoundError(dataset)

        users = {}
        edges = []

        count = 0

        print("Importing dataset...\n")

        with gzip.open(dataset, "rt", encoding="utf-8") as f:

            for line in f:

                if line.startswith("#"):
                    continue

                src, dst = map(int, line.strip().split())

                users[src] = {
                    "_key": str(src)
                }

                users[dst] = {
                    "_key": str(dst)
                }

                edges.append(
                    {
                        "_from": f"users/{src}",
                        "_to": f"users/{dst}",
                    }
                )

                count += 1

                if len(edges) >= BATCH_SIZE:

                    self.flush(users, edges)

                    users = {}
                    edges = []

                    if count % 10000 == 0:
                        print(f"Imported {count:,} relationships")

                if count >= MAX_RELATIONSHIPS:
                    break

        if edges:
            self.flush(users, edges)

        print("\n" + "=" * 50)
        print("ArangoDB Import Completed")
        print("=" * 50)
        print(f"Relationships Imported : {count:,}")


if __name__ == "__main__":

    importer = ArangoImporter()

    importer.import_dataset()