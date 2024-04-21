from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from ...services.twitter import service_twitter_fetch_top_posts, service_twitter_fetch_people, service_twitter_fetch_latest_posts, service_twitter_user_following_list, service_twitter_user_follower_list, service_twitter_user_posts
from ...utils import twitter_db_operation

class TwitterCreds(BaseModel):
    username: str
    password: str

class TwitterQuery(BaseModel):
    query_string: str
    query_length: int

class UserFollowQuery(TwitterQuery):
    verification_filter: bool


router = APIRouter(
    prefix= "/api/v1/twitter",
    tags = ["twitterDataFetch"],
    responses= {404 : {"description" : "Path Not found"}},
)


@router.post("/fetchTopTweets")
def fetch__top_twitter_posts(data: TwitterQuery):
    result = service_twitter_fetch_top_posts.driver_function(data)
    return result

@router.post("/fetchPeopleList")
def fetch_people_list(data: TwitterQuery):
    result = service_twitter_fetch_people.driver_function(data)
    return result

@router.post("/fetchLatestTweets")
def fetch_latest_twitter_posts(data: TwitterQuery):
    result = service_twitter_fetch_latest_posts.driver_function(data)
    return result

@router.post("/fetchFollowingList")
def fetch_account_following_list(data: TwitterQuery):
    result = service_twitter_user_following_list.driver_function(data)
    return result

@router.post("/fetchFollowerList")
def fetch_account_follower_list(data: UserFollowQuery):
    result = service_twitter_user_follower_list.driver_function(data)
    return result

@router.post("/fetchUserSpecificTweets")
def fetch_user_specific_tweets(data: TwitterQuery):
    result = service_twitter_user_posts.driver_function(data)
    return result


@router.post("/loadCreds")
def load_data_to_db(data: TwitterCreds):
    result = twitter_db_operation.load_data_to_db(service_name="twitter",data=data)
    return result



