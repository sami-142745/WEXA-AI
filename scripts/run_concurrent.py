from benchmark.concurrent_runner import ConcurrentBenchmark
from benchmark.connectors.factory import ConnectorFactory
from benchmark.exporter import ResultExporter
from benchmark.results import results

DATABASES = [
    "cognodb",
    "neo4j",
    "memgraph",
    "arangodb",
    "age",
]


def print_result(name, result):
    print("\n" + name)
    print("-" * 40)
    print(f"Workers     : {result['Workers']}")
    print(f"Iterations  : {result['Iterations']}")
    print(f"Total Time  : {result['Total Time']:.2f} sec")
    print(f"Throughput  : {result['Throughput']:.2f} ops/sec")


def main():

    benchmark = ConcurrentBenchmark(
        workers=10,
        iterations=100,
    )

    for db_name in DATABASES:

        print("\n" + "=" * 60)
        print(db_name.upper())
        print("=" * 60)

        try:

            db = ConnectorFactory.get(db_name)

            db.connect()
            db.verify()

            # ---------------------------------------
            # Concurrent Lookup
            # ---------------------------------------

            lookup_result = benchmark.run(
                db.lookup,
                database=db_name,
                workload_name="Concurrent Lookup",
            )

            results.add_concurrent(
                database=db_name,
                workload="Concurrent Lookup",
                workers=lookup_result["Workers"],
                iterations=lookup_result["Iterations"],
                total_time=lookup_result["Total Time"],
                throughput=lookup_result["Throughput"],
            )

            print_result(
                "Concurrent Lookup",
                lookup_result,
            )

            # ---------------------------------------
            # Concurrent Traversal
            # ---------------------------------------

            traversal_result = benchmark.run(
                db.traversal_1hop,
                database=db_name,
                workload_name="Concurrent Traversal",
            )

            results.add_concurrent(
                database=db_name,
                workload="Concurrent Traversal",
                workers=traversal_result["Workers"],
                iterations=traversal_result["Iterations"],
                total_time=traversal_result["Total Time"],
                throughput=traversal_result["Throughput"],
            )

            print_result(
                "Concurrent Traversal",
                traversal_result,
            )

            db.close()

        except Exception as e:

            print(f"\nFAILED : {db_name}")
            print(type(e).__name__)
            print(e)

    # ---------------------------------------
    # Export Concurrent Results
    # ---------------------------------------

    print("\nExporting Concurrent Results...")

    exporter = ResultExporter(results)

    exporter.export_concurrent()

    print("Concurrent Results Saved Successfully.")
    print("Location : results/")


if __name__ == "__main__":
    main()