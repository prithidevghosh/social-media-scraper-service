from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from ...services.twitter import service_twitter
from ...utils import twitter_db_operation

class Twitter(BaseModel):
    username: str
    password: str


router = APIRouter(
    prefix= "/api/v1/twitter",
    tags = ["twitterDataFetch"],
    responses= {404 : {"description" : "Path Not found"}},
)


@router.post("/fetchPosts")
def fetch_twitter_posts(data: Twitter):
    result = service_twitter.driver_function(data)
    return result

@router.post("/loadCreds")
def load_data_to_db(data: Twitter):
    result = twitter_db_operation.load_data_to_db(service_name="twitter",data=data)
    return result



