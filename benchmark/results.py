from dataclasses import dataclass, asdict
from typing import List


@dataclass
class BenchmarkRecord:
    database: str
    workload: str
    average: float
    minimum: float
    maximum: float
    p50: float
    p95: float
    iterations: int
    warmup: int


@dataclass
class ConcurrentRecord:
    database: str
    workload: str
    workers: int
    iterations: int
    total_time: float
    throughput: float


@dataclass
class ImportRecord:
    database: str
    nodes: int
    relationships: int
    total_time: float
    nodes_per_second: float
    relationships_per_second: float


class BenchmarkResults:

    def __init__(self):

        self.benchmarks: List[BenchmarkRecord] = []
        self.concurrent: List[ConcurrentRecord] = []
        self.imports: List[ImportRecord] = []

    # --------------------------------------------------
    # Benchmark Results
    # --------------------------------------------------

    def add_benchmark(
        self,
        database,
        workload,
        average,
        minimum,
        maximum,
        p50,
        p95,
        iterations,
        warmup,
    ):

        self.benchmarks.append(
            BenchmarkRecord(
                database,
                workload,
                average,
                minimum,
                maximum,
                p50,
                p95,
                iterations,
                warmup,
            )
        )

    # --------------------------------------------------
    # Concurrent Results
    # --------------------------------------------------

    def add_concurrent(
        self,
        database,
        workload,
        workers,
        iterations,
        total_time,
        throughput,
    ):

        self.concurrent.append(
            ConcurrentRecord(
                database,
                workload,
                workers,
                iterations,
                total_time,
                throughput,
            )
        )

    # --------------------------------------------------
    # Import Results
    # --------------------------------------------------

    def add_import(
        self,
        database,
        nodes,
        relationships,
        total_time,
        nodes_per_second,
        relationships_per_second,
    ):

        self.imports.append(
            ImportRecord(
                database,
                nodes,
                relationships,
                total_time,
                nodes_per_second,
                relationships_per_second,
            )
        )

    # --------------------------------------------------
    # Export Helpers
    # --------------------------------------------------

    def benchmark_dict(self):

        return [
            asdict(record)
            for record in self.benchmarks
        ]

    def concurrent_dict(self):

        return [
            asdict(record)
            for record in self.concurrent
        ]

    def import_dict(self):

        return [
            asdict(record)
            for record in self.imports
        ]


results = BenchmarkResults()