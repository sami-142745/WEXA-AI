import traceback

from benchmark.connectors.factory import ConnectorFactory
from benchmark.benchmark_runner import BenchmarkRunner
from benchmark.exporter import ResultExporter
from benchmark.results import results

DATABASES = [
    "cognodb",
    "neo4j",
    "memgraph",
    "arangodb",
    "age",
]


def print_results(result):
    print(f"Average   : {result['Average']:.2f} ms")
    print(f"Minimum   : {result['Minimum']:.2f} ms")
    print(f"Maximum   : {result['Maximum']:.2f} ms")
    print(f"P50       : {result['P50']:.2f} ms")
    print(f"P95       : {result['P95']:.2f} ms")
    print(f"Iterations: {result['Iterations']}")
    print(f"Warmup    : {result['Warmup']}")


def main():

    print("\nStarting Benchmark...\n")

    runner = BenchmarkRunner()

    for database in DATABASES:

        print("=" * 70)
        print(f"Database : {database.upper()}")
        print("=" * 70)

        try:

            db = ConnectorFactory.get(database)

            db.connect()
            db.verify()

            print("Connection Successful")

            workloads = [
                ("Node Count", db.node_count),
                ("Lookup", db.lookup),
                ("Traversal 1-Hop", db.traversal_1hop),
            ]

            # Run 2-Hop if connector supports it
            if hasattr(db, "traversal_2hop"):
                workloads.append(("Traversal 2-Hop", db.traversal_2hop))

            # Run 3-Hop if connector supports it
            if hasattr(db, "traversal_3hop"):
                workloads.append(("Traversal 3-Hop", db.traversal_3hop))

            workloads.append(("Aggregation", db.aggregation))

            for workload_name, workload in workloads:

                print("\n" + "-" * 50)
                print(workload_name)
                print("-" * 50)

                try:

                    result = runner.run(
                        workload,
                        database=database,
                        workload=workload_name,
                    )

                    print_results(result)

                except Exception as e:

                    print(f"FAILED : {workload_name}")
                    print(type(e).__name__)
                    print(e)
                    traceback.print_exc()

            db.close()

        except Exception as e:

            print(f"FAILED : {database}")
            print(type(e).__name__)
            print(e)
            traceback.print_exc()

    print("\nExporting Results...")

    exporter = ResultExporter(results)

    exporter.export_all()

    print("\nBenchmark Finished Successfully.")
    print("Results saved in ./results/")


if __name__ == "__main__":
    main()