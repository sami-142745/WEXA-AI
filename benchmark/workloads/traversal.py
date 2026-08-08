import random
from benchmark.connectors.cognodb import CognoDBConnector


class TraversalBenchmark:

    def __init__(self):
        self.db = CognoDBConnector()
        self.db.connect()
        self.db.verify()

        print("Loading sample node IDs...")

        rows = self.db.execute("""
        MATCH (u:User)
        RETURN u.id AS id
        LIMIT 5000
        """)

        self.ids = [r["id"] for r in rows]

    def traversal(self, hops):

        node = random.choice(self.ids)

        query = f"""
        MATCH (u:User {{id:$id}})
        MATCH p=(u)-[:FRIEND*{hops}]->()
        RETURN count(p)
        """

        self.db.execute(query, {"id": node})

    def close(self):
        self.db.close()