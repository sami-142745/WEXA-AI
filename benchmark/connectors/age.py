import random
import psycopg2

from benchmark.connectors.base import BaseConnector
from benchmark.config import (
    AGE_HOST,
    AGE_PORT,
    AGE_DATABASE,
    AGE_USER,
    AGE_PASSWORD,
)

GRAPH_NAME = "cognodb"


class AgeConnector(BaseConnector):

    def __init__(self):
        self.conn = None

    def connect(self):

        self.conn = psycopg2.connect(
            host=AGE_HOST,
            port=int(AGE_PORT),
            database=AGE_DATABASE,
            user=AGE_USER,
            password=AGE_PASSWORD,
        )

        self.conn.autocommit = False

        cur = self.conn.cursor()
        cur.execute("LOAD 'age';")
        cur.execute('SET search_path = ag_catalog, "$user", public;')
        self.conn.commit()
        cur.close()

    def verify(self):

        cur = self.conn.cursor()
        cur.execute("SELECT version();")
        print(cur.fetchone()[0])
        cur.close()

    def execute(self, query, parameters=None):

        # Create a NEW connection for every thread
        conn = psycopg2.connect(
            host=AGE_HOST,
            port=int(AGE_PORT),
            database=AGE_DATABASE,
            user=AGE_USER,
            password=AGE_PASSWORD,
        )

        conn.autocommit = False

        cur = conn.cursor()

        try:

            cur.execute("LOAD 'age';")
            cur.execute('SET search_path = ag_catalog, "$user", public;')

            cur.execute(query, parameters or ())

            rows = []

            if cur.description is not None:
                rows = cur.fetchall()

            conn.commit()

            return rows

        except Exception:

            conn.rollback()
            raise

        finally:

            cur.close()
            conn.close()

    def execute_read(self, query, parameters=None):
        return self.execute(query, parameters)

    def execute_write(self, query, parameters=None):
        return self.execute(query, parameters)

    def close(self):

        if self.conn:
            self.conn.close()

    # ---------------------------------------------------
    # Benchmarks
    # ---------------------------------------------------

    def node_count(self):

        query = f"""
        SELECT *
        FROM cypher('{GRAPH_NAME}', $$
            MATCH (n)
            RETURN count(n)
        $$) AS (count agtype);
        """

        return self.execute(query)

    def lookup(self):

        node_id = random.randint(1, 1000)

        query = f"""
        SELECT *
        FROM cypher('{GRAPH_NAME}', $$
            MATCH (n {{id:{node_id}}})
            RETURN n
        $$) AS (node agtype);
        """

        return self.execute(query)

    def traversal_1hop(self):

        node_id = random.randint(1, 1000)

        query = f"""
        SELECT *
        FROM cypher('{GRAPH_NAME}', $$
            MATCH (n {{id:{node_id}}})-[]->(m)
            RETURN m
        $$) AS (node agtype);
        """

        return self.execute(query)

    def traversal_2hop(self):

        node_id = random.randint(1, 1000)

        query = f"""
        SELECT *
        FROM cypher('{GRAPH_NAME}', $$
            MATCH (n {{id:{node_id}}})-[]->()-[]->(m)
            RETURN m
        $$) AS (node agtype);
        """

        return self.execute(query)

    def traversal_3hop(self):

        node_id = random.randint(1, 1000)

        query = f"""
        SELECT *
        FROM cypher('{GRAPH_NAME}', $$
            MATCH (n {{id:{node_id}}})-[]->()-[]->()-[]->(m)
            RETURN m
        $$) AS (node agtype);
        """

        return self.execute(query)

    def aggregation(self):

        query = f"""
        SELECT *
        FROM cypher('{GRAPH_NAME}', $$
            MATCH (n)
            RETURN labels(n), count(*)
        $$) AS (label agtype, total agtype);
        """

        return self.execute(query)