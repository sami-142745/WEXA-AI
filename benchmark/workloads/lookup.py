import random
from benchmark.connectors.cognodb import CognoDBConnector


class LookupBenchmark:

    def __init__(self):
        self.db = CognoDBConnector()
        self.db.connect()
        self.db.verify()

        rows = self.db.execute("""
        MATCH (u:User)
        RETURN u.id AS id
        LIMIT 5000
        """)

        self.ids = [r["id"] for r in rows]

    def point_lookup(self):
        node = random.choice(self.ids)

        self.db.execute("""
        MATCH (u:User {id:$id})
        RETURN u
        """, {"id": node})

    def indexed_lookup(self):
        node = random.choice(self.ids)

        self.db.execute("""
        MATCH (u:User)
        WHERE u.id=$id
        RETURN u
        """, {"id": node})

    def close(self):
        self.db.close()