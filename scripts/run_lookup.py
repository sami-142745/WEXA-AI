from benchmark.reporting.json_export import JSONExporter
from benchmark.reporting.csv_export import CSVExporter
from benchmark.benchmark_runner import BenchmarkRunner
from benchmark.workloads.lookup import LookupBenchmark

bench = LookupBenchmark()
runner = BenchmarkRunner()

# -----------------------------
# POINT LOOKUP
# -----------------------------
print("POINT LOOKUP")

point = runner.run(bench.point_lookup)

print(f"Average : {point['Average']} ms")
print(f"P50     : {point['P50']} ms")
print(f"P95     : {point['P95']} ms")

CSVExporter.save("point_lookup.csv", point)
JSONExporter.save("point_lookup.json", point)

print()

# -----------------------------
# INDEXED LOOKUP
# -----------------------------
print("INDEXED LOOKUP")

indexed = runner.run(bench.indexed_lookup)

print(f"Average : {indexed['Average']} ms")
print(f"P50     : {indexed['P50']} ms")
print(f"P95     : {indexed['P95']} ms")

CSVExporter.save("indexed_lookup.csv", indexed)
JSONExporter.save("indexed_lookup.json", indexed)

bench.close()