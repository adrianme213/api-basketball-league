from pymongo import MongoClient

DB_HOST = ""
DB_USERNAME = ""
DB_PASSWORD = ""
DB_URL = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/myFirstDatabase?retryWrites=true&w=majority"


def get_db_connection():
    client = MongoClient(DB_URL)
    return client
