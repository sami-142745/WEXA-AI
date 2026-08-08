import time
from concurrent.futures import ThreadPoolExecutor

from benchmark.results import results


class ConcurrentBenchmark:

    def __init__(self, workers=10, iterations=100):
        self.workers = workers
        self.iterations = iterations

    def run(self, workload, database=None, workload_name=None):

        start = time.perf_counter()

        with ThreadPoolExecutor(max_workers=self.workers) as executor:

            futures = [
                executor.submit(workload)
                for _ in range(self.iterations)
            ]

            for future in futures:
                future.result()

        elapsed = time.perf_counter() - start

        throughput = self.iterations / elapsed

        result = {
            "Workers": self.workers,
            "Iterations": self.iterations,
            "Total Time": round(elapsed, 2),
            "Throughput": round(throughput, 2),
        }

        # ---------------------------------------
        # Automatically save concurrent results
        # ---------------------------------------

        if database is not None and workload_name is not None:

            results.add_concurrent(
                database=database,
                workload=workload_name,
                workers=self.workers,
                iterations=self.iterations,
                total_time=result["Total Time"],
                throughput=result["Throughput"],
            )

        return result