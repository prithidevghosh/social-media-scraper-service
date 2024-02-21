from fastapi import FastAPI
from fastapi.logger import logger
from apscheduler.schedulers.background import BackgroundScheduler
#import asyncio

from app.routes.twitter import route_twitter
app = FastAPI(title='ScrapHead', description='social media scraper micro services', version='0.1', docs_url="/documentation", redoc_url=None)

@app.get("/info")
def root():
    return {"service": "social media scraper service",
            "version": "0.1"}


app.include_router(route_twitter.router)