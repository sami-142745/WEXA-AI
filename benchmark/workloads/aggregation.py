from benchmark.connectors.cognodb import CognoDBConnector


class AggregationBenchmark:

    def __init__(self):

        self.db = CognoDBConnector()

        self.db.connect()

        self.db.verify()

    def run(self):

        self.db.execute("""
        MATCH (u:User)-[:FRIEND]->()

        RETURN count(u)
        """)

    def close(self):

        self.db.close()