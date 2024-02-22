from ..config import mongo_config
from ..utils import logger
from pymongo.errors import PyMongoError
from ..utils.error_msg_struct import fetch_error_message_struct

DB_NAME = "social-media-scraping-service"
TWITTER_CREDS_COLLECTION_NAME = "creds-twitter"

def retrieve_user_creds(service_name):
    client = mongo_config.get_mongo_client()
    db = client[DB_NAME]

    if service_name == "twitter":
        logger.info(f"**hitting db of collection name: {TWITTER_CREDS_COLLECTION_NAME}")
        collection = db[TWITTER_CREDS_COLLECTION_NAME]
        result = collection.find({})
            

        if result:
            logger.info("**got result from DB")
            return result
        else:
            logger.error("**error in fetching results from DB")
            return fetch_error_message_struct(status_code=500)

def load_data_to_db(service_name, data):
    client = mongo_config.get_mongo_client()
    db = client[DB_NAME]

    if service_name == "twitter":
        try:
            username = str(data.username).strip()
            password = str(data.password).strip()
            collection = db[TWITTER_CREDS_COLLECTION_NAME]
            collection.insert_one({"username":username, "password":password})
            
            return fetch_error_message_struct(status_code=200)


        except PyMongoError as e:
            logger.error("**error while loading creds in twitter db")
            return fetch_error_message_struct(status_code=500)





