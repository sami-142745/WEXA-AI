from benchmark.reporting.json_export import JSONExporter
from benchmark.reporting.csv_export import CSVExporter
from benchmark.workloads.aggregation import AggregationBenchmark
from benchmark.benchmark_runner import BenchmarkRunner

bench = AggregationBenchmark()

runner = BenchmarkRunner()

result = runner.run(bench.run)

print()

print("=" * 40)
print("AGGREGATION")
print("=" * 40)

for k, v in result.items():

    if k != "Samples":
        print(k, ":", v)
CSVExporter.save("aggregation.csv", result)
JSONExporter.save("aggregation.json", result)
bench.close()
