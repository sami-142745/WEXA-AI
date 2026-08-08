import time


class LoadingBenchmark:

    def __init__(self):
        self.start = None

    def begin(self):
        self.start = time.perf_counter()

    def end(self, nodes, relationships):

        elapsed = time.perf_counter() - self.start

        return {
            "Load Time (s)": round(elapsed, 2),
            "Nodes/sec": round(nodes / elapsed, 2),
            "Relationships/sec": round(relationships / elapsed, 2),
        }