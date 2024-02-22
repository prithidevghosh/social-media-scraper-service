import os
import pymongo

def get_mongo_client():

    return pymongo.MongoClient("mongodb://localhost:27017")