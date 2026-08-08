from arango import ArangoClient
import random

from benchmark.connectors.base import BaseConnector
from benchmark.config import (
    ARANGODB_URL,
    ARANGODB_DATABASE,
    ARANGODB_USER,
    ARANGODB_PASSWORD,
)


class ArangoDBConnector(BaseConnector):

    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        self.client = ArangoClient(hosts=ARANGODB_URL)

        self.db = self.client.db(
            ARANGODB_DATABASE,
            username=ARANGODB_USER,
            password=ARANGODB_PASSWORD,
        )

    def verify(self):
        print("Connected to ArangoDB")
        print("Version:", self.db.version())

    def execute(self, query, parameters=None):
        cursor = self.db.aql.execute(
            query,
            bind_vars=parameters or {}
        )
        return list(cursor)

    def execute_read(self, query, parameters=None):
        return self.execute(query, parameters)

    def execute_write(self, query, parameters=None):
        return self.execute(query, parameters)

    def close(self):
        pass

    # -------------------------------------------------
    # Benchmark Methods
    # -------------------------------------------------

    def node_count(self):
        return self.execute("""
        RETURN LENGTH(users)
        """)

    def lookup(self):
        node = random.randint(1, 40000)

        return self.execute("""
        FOR u IN users
            FILTER u._key == @id
            RETURN u
        """, {"id": str(node)})

    def traversal_1hop(self):

        node = random.randint(1, 40000)

        query = """
        WITH users

        FOR v, e, p IN 1..1
            OUTBOUND @start
            friends
        RETURN v
        """

        return self.execute(
            query,
            {
                "start": f"users/{node}"
            }
        )

    def traversal_2hop(self):

        node = random.randint(1, 40000)

        query = """
        WITH users

        FOR v, e, p IN 1..2
            OUTBOUND @start
            friends
        RETURN v
        """

        return self.execute(
            query,
            {
                "start": f"users/{node}"
            }
        )

    def traversal_3hop(self):

        node = random.randint(1, 40000)

        query = """
        WITH users

        FOR v, e, p IN 1..3
            OUTBOUND @start
            friends
        RETURN v
        """

        return self.execute(
            query,
            {
                "start": f"users/{node}"
            }
        )

    def aggregation(self):
        return self.execute("""
        RETURN LENGTH(friends)
        """)