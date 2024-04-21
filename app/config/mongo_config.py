import os
import pymongo

DB_ENV = os.environ.get("ENVIRONMENT")
REMOTE_MONGO_SERVER = os.environ.get("DB_CRED")

def get_mongo_client():
    if DB_ENV == "local":
        return pymongo.MongoClient("mongodb://localhost:27017")
    elif DB_ENV == "staging":
        return pymongo.MongoClient(REMOTE_MONGO_SERVER)

