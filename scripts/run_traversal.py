from benchmark.benchmark_runner import BenchmarkRunner
from benchmark.workloads.traversal import TraversalBenchmark
from benchmark.reporting.csv_export import CSVExporter
from benchmark.reporting.json_export import JSONExporter

bench = TraversalBenchmark()
runner = BenchmarkRunner(warmup=20, iterations=100)

all_results = {}

for hop in [1, 2, 3]:

    print("\n" + "=" * 50)
    print(f"{hop}-HOP TRAVERSAL")
    print("=" * 50)

    result = runner.run(lambda: bench.traversal(hop))

    print(f"Average : {result['Average']} ms")
    print(f"Minimum : {result['Minimum']} ms")
    print(f"Maximum : {result['Maximum']} ms")
    print(f"P50     : {result['P50']} ms")
    print(f"P95     : {result['P95']} ms")

    CSVExporter.save(f"traversal_{hop}_hop.csv", result)
    JSONExporter.save(f"traversal_{hop}_hop.json", result)

    all_results[f"{hop}-Hop"] = result

bench.close()