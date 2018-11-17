from abc import ABC, abstractmethod
from typing import Dict

__names__ = ["AbstractDatabase", "TABLE_NAME", "DB_NAME"]

DB_NAME = "wqadb"
TABLE_NAME = "corpus"


class AbstractDatabase(ABC):
    default_uri: str

    def __init__(self, uri):
        self.uri = uri
        self.client = None
        super().__init__()

    @abstractmethod
    def create_db(self):
        pass

    @abstractmethod
    def connect_db(self):
        pass

    @abstractmethod
    def drop_db(self):
        pass

    @abstractmethod
    def start_transaction(self):
        pass

    @abstractmethod
    def insert_many(self, items: [Dict[str, str]]) -> [Dict[str, str]]:
        pass
