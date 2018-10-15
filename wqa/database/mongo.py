from typing import Dict

from pymongo import MongoClient

from wqa.database import AbstractDatabase, DB_NAME, TABLE_NAME


class MongoDatabase(AbstractDatabase):
    default_uri = "mongodb://localhost:27017/"

    def create_db(self):
        pass

    def connect_db(self):
        self.client = MongoClient(self.uri)

    def drop_db(self):
        db = self.client[DB_NAME]
        db.drop_collection(TABLE_NAME)

    def insert_many(self, items: [Dict[str, str]]) -> [Dict[str, str]]:
        db = self.client[DB_NAME]
        inserted = db[TABLE_NAME].insert_many(items)
        return inserted
