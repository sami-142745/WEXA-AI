import time

from benchmark.results import results


class ImportMetrics:

    def __init__(self, database):
        self.database = database
        self.start = None

    def begin(self):
        self.start = time.perf_counter()

    def finish(self, nodes, relationships):

        elapsed = time.perf_counter() - self.start

        nodes_per_second = (
            nodes / elapsed if elapsed else 0
        )

        rels_per_second = (
            relationships / elapsed if elapsed else 0
        )

        print("\n" + "=" * 60)
        print(f"{self.database.upper()} IMPORT SUMMARY")
        print("=" * 60)

        print(f"Nodes             : {nodes:,}")
        print(f"Relationships     : {relationships:,}")
        print(f"Import Time       : {elapsed:.2f} sec")
        print(f"Nodes/sec         : {nodes_per_second:.2f}")
        print(f"Relationships/sec : {rels_per_second:.2f}")

        results.add_import(
            database=self.database,
            nodes=nodes,
            relationships=relationships,
            total_time=elapsed,
            nodes_per_second=nodes_per_second,
            relationships_per_second=rels_per_second,
        )