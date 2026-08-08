# from neo4j import GraphDatabase

# from benchmark.config import (
#     COGNODB_URI,
#     COGNODB_USER,
#     COGNODB_PASSWORD,
# )

# from benchmark.connectors.base import BaseConnector


# class CognoDBConnector(BaseConnector):

#     def __init__(self):
#         self.driver = None

#     def connect(self):
#         self.driver = GraphDatabase.driver(
#             COGNODB_URI,
#             auth=(COGNODB_USER, COGNODB_PASSWORD),
#         )

#     def verify(self):
#         self.driver.verify_connectivity()

#     def execute(self, query, parameters=None):
#         with self.driver.session() as session:
#             result = session.run(query, parameters or {})
#             return list(result)

#     def execute_read(self, query, parameters=None):
#         return self.execute(query, parameters)

#     def execute_write(self, query, parameters=None):
#         return self.execute(query, parameters)

#     def close(self):
#         if self.driver:
#             self.driver.close()

from neo4j import GraphDatabase
import random

from benchmark.config import (
    COGNODB_URI,
    COGNODB_USER,
    COGNODB_PASSWORD,
)

from benchmark.connectors.base import BaseConnector


class CognoDBConnector(BaseConnector):

    def __init__(self):
        self.driver = None

    def connect(self):
        self.driver = GraphDatabase.driver(
            COGNODB_URI,
            auth=(COGNODB_USER, COGNODB_PASSWORD),
        )

    def verify(self):
        self.driver.verify_connectivity()

    def execute(self, query, parameters=None):
        with self.driver.session() as session:
            return list(session.run(query, parameters or {}))

    def execute_read(self, query, parameters=None):
        return self.execute(query, parameters)

    def execute_write(self, query, parameters=None):
        return self.execute(query, parameters)

    def close(self):
        if self.driver:
            self.driver.close()

    # -----------------------------
    # Standard Benchmark Workloads
    # -----------------------------

    def node_count(self):
        return self.execute("""
        MATCH (n)
        RETURN count(n) AS total
        """)

    def traversal_1hop(self):
        node = random.randint(1, 40000)

        return self.execute("""
        MATCH (u:User {id:$id})-[:FRIEND]->(v)
        RETURN count(v)
        """, {"id": node})

    def lookup(self):
        node = random.randint(1, 40000)

        return self.execute("""
        MATCH (u:User {id:$id})
        RETURN u
        """, {"id": node})

    def aggregation(self):
        return self.execute("""
        MATCH (u:User)-[:FRIEND]->()
        RETURN count(u) AS total
        """)