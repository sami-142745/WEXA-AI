from neo4j import GraphDatabase
import random

from benchmark.connectors.base import BaseConnector
from benchmark.config import (
    NEO4J_URI,
    NEO4J_USER,
    NEO4J_PASSWORD,
)


class Neo4jConnector(BaseConnector):

    def __init__(self):
        self.driver = None

    def connect(self):
        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD),
        )

    def verify(self):
        self.driver.verify_connectivity()
        print("Connected to Neo4j")

    def execute(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return list(result)

    def execute_read(self, query, parameters=None):
        return self.execute(query, parameters)

    def execute_write(self, query, parameters=None):
        return self.execute(query, parameters)

    def close(self):
        if self.driver:
            self.driver.close()

    # -------------------------
    # Benchmark Workloads
    # -------------------------

    def node_count(self):
        return self.execute("""
        MATCH (n)
        RETURN count(n) AS total
        """)

    def lookup(self):
        node = random.randint(1, 40000)

        return self.execute("""
        MATCH (u:User {id:$id})
        RETURN u
        """, {"id": node})

    def traversal_1hop(self):
        node = random.randint(1, 40000)

        return self.execute("""
        MATCH (u:User {id:$id})-[:FRIEND]->(v)
        RETURN count(v) AS total
        """, {"id": node})

    def traversal_2hop(self):
        node = random.randint(1, 40000)

        return self.execute("""
        MATCH (u:User {id:$id})-[:FRIEND*2]->(v)
        RETURN count(v) AS total
        """, {"id": node})

    def traversal_3hop(self):
        node = random.randint(1, 40000)

        return self.execute("""
        MATCH (u:User {id:$id})-[:FRIEND*3]->(v)
        RETURN count(v) AS total
        """, {"id": node})

    def aggregation(self):
        return self.execute("""
        MATCH (u:User)-[:FRIEND]->()
        RETURN count(u) AS total
        """)