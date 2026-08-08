from benchmark.connectors.cognodb import CognoDBConnector
from benchmark.connectors.neo4j import Neo4jConnector
from benchmark.connectors.memgraph import MemgraphConnector
from benchmark.connectors.arangodb import ArangoDBConnector
from benchmark.connectors.age import AgeConnector


class ConnectorFactory:

    CONNECTORS = {
        "cognodb": CognoDBConnector,
        "neo4j": Neo4jConnector,
        "memgraph": MemgraphConnector,
        "arangodb": ArangoDBConnector,
        "age": AgeConnector,
    }

    @staticmethod
    def get(name):
        name = name.lower()

        if name not in ConnectorFactory.CONNECTORS:
            raise ValueError(f"Unsupported database: {name}")

        return ConnectorFactory.CONNECTORS[name]()