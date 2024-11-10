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
        if len(db) == 0:
            # Insert default tokens or initial empty tokens if db.json is empty
            DbManager.insert_token({
                "strava_access_token": os.getenv("STRAVA_ACCESS_TOKEN"),
                "strava_refresh_token": os.getenv("STRAVA_REFRESH_TOKEN"),
                "spotify_access_token": os.getenv("SPOTIFY_ACCESS_TOKEN"),
                "spotify_refresh_token": os.getenv("STRAVA_REFRESH_TOKEN"),
            })
        token = db.all()
        return token[0]

    @staticmethod
    def update_token(data):
        return db.update(data)
    


