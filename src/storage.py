from tinydb import TinyDB, Query
import os

db = TinyDB("./db.json")

TokenInfo = Query()


class DbManager:
    @staticmethod
    def insert_token(data):
        if len(db) == 0:
            return db.insert(
                data
            )
        return None

    @staticmethod
    def get_token():
        token = db.all()
        return token[0]

    @staticmethod
    def update_token(data):
        return db.update(data)
    


