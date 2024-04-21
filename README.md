# social-media-scraper-service

The Social Media Scraper Service provides functionality to scrape various social media sites like Twitter, Instagram, Facebook, etc. As of now, only the Twitter scraper is implemented. Below, you'll find a detailed guide on how to interact with the API, key features, and example requests.

**Warning:** This product is still in development thus to try this you need to run the app locally. It's very easy to setup not complex as other open source projects :). 
**Usage Info** Please use this [Postman collection](https://api.postman.com/collections/26116850-a011a2b0-5717-46f4-9c03-2f4b3e47ac0e?access_key=PMAT-01HW1271WHY7TTEYNAFFZSDTZB) to access the API curls.



<h3><i>Prerequisites</i></h3>
<ul>
<li>MongoDB v4.4 or higher</li>
</ul>


*steps to locally configure and run this app*


## Clone the repo
```bash

git clone https://github.com/prithidevghosh/social-media-scraper-service.git


```
## Install the required packages
```bash

pip install -r requirements.txt

```

## Start the server locally
```bash

uvicorn app.main:app --reload

```


<h3><i>Configuration</i></h3>

<p>The application requires a MongoDB instance to be set up. You can configure the database connection by setting the following environment variables:</p>

```bash

DB_CRED = "your mongo cluster URI"
ENVIRONMENT = "local" or "staging"

```

<h3><i>API Endpoints</i></h3>


| Endpoint Name | Method | Purpose |
| --- | --- | --- |
| `/fetchTopTweets` | POST | fetch top tweets related a search query, limit the search result length as well |
| `/fetchPeopleList` | POST | fetch people list related a search query, limit the search result length as well |
| `/fetchLatestTweets` | POST | fetch latest tweets related a search query, limit the search result length as well |
| `/fetchFollowingList` | POST | fetch following list of an user account, limit the search result length as well |
| `/fetchFollowerList` | POST | fetch foller list of an user account, limit the search result length as well |



```


