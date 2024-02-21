from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from ...services.twitter import service_twitter

class Twitter(BaseModel):
    username: str
    password: str


router = APIRouter(
    prefix= "/api/v1/twitter",
    tags = ["twitterDataFetch"],
    responses= {404 : {"description" : "Path Not found"}},
)


@router.post("/fetchPosts")
def fetchTwitterPosts(data: Twitter):
    result = service_twitter.driver_function(data)
    return result


