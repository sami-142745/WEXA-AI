from abc import ABC, abstractmethod


class BaseConnector(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def verify(self):
        pass

    @abstractmethod
    def execute(self, query, parameters=None):
        pass

    @abstractmethod
    def close(self):
        pass

    # ---------- Standard workloads ----------

    @abstractmethod
    def node_count(self):
        pass

    @abstractmethod
    def traversal_1hop(self):
        pass

    @abstractmethod
    def lookup(self):
        pass

    @abstractmethod
    def aggregation(self):
        pass