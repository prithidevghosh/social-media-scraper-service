

from .logger import logger



BEARER_TOKEN = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

SERVICE_NAME = "TWITTER-FETCH-USER-ID"

def fetch_user_id(session, x_csrf_token, username):
    logger.info(f"***{SERVICE_NAME}::: fetching user id for the username: {username}")

    url = f"https://twitter.com/i/api/graphql/k5XapwcSikNsEsILW5FvgA/UserByScreenName?variables=%7B%22screen_name%22%3A%22{username}%22%2C%22withSafetyModeUserFields%22%3Atrue%7D&features=%7B%22hidden_profile_likes_enabled%22%3Atrue%2C%22hidden_profile_subscriptions_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22subscriptions_verification_info_is_identity_verified_enabled%22%3Atrue%2C%22subscriptions_verification_info_verified_since_enabled%22%3Atrue%2C%22highlights_tweets_tab_ui_enabled%22%3Atrue%2C%22responsive_web_twitter_article_notes_tab_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D&fieldToggles=%7B%22withAuxiliaryUserLabels%22%3Afalse%7D"

    payload = {}
    headers = {
    'Host': 'twitter.com',
    'Sec-Ch-Ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
    'X-Twitter-Client-Language': 'en',
    'X-Csrf-Token': f'{x_csrf_token}',
    'Sec-Ch-Ua-Mobile': '?0',
    'Authorization': f'{BEARER_TOKEN}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.199 Safari/537.36',
    'Content-Type': 'application/json',
    'X-Twitter-Auth-Type': 'OAuth2Session',
    'X-Twitter-Active-User': 'yes',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Accept': '/',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': f'https://twitter.com/{username}',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Priority': 'u=1, i',
    }

    response = session.get(url, headers=headers, data=payload)

    json_response = response.json()

    user_id =  json_response.get("data").get("user").get("result").get("rest_id")

    return user_id