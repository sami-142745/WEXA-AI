import time

from benchmark.metrics.statistics import Statistics
from benchmark.results import results


class BenchmarkRunner:

    def __init__(self, warmup=20, iterations=100):
        self.warmup = warmup
        self.iterations = iterations

    def run(self, func, database=None, workload=None):

        # Warmup
        for _ in range(self.warmup):
            func()

        samples = []

        # Benchmark
        for _ in range(self.iterations):

            start = time.perf_counter()

            func()

            end = time.perf_counter()

            samples.append((end - start) * 1000)

        result = {
            "Average": round(Statistics.average(samples), 2),
            "Minimum": round(Statistics.minimum(samples), 2),
            "Maximum": round(Statistics.maximum(samples), 2),
            "P50": round(Statistics.percentile(samples, 50), 2),
            "P95": round(Statistics.percentile(samples, 95), 2),
            "Iterations": self.iterations,
            "Warmup": self.warmup,
            "Samples": samples,
        }

        # Automatically save benchmark
        if database is not None and workload is not None:

            results.add_benchmark(
                database=database,
                workload=workload,
                average=result["Average"],
                minimum=result["Minimum"],
                maximum=result["Maximum"],
                p50=result["P50"],
                p95=result["P95"],
                iterations=result["Iterations"],
                warmup=result["Warmup"],
            )

        return result