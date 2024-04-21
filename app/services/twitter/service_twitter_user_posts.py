import requests
import json
import math
from datetime import datetime


from ...utils.logger import logger
from ...utils.fetch_user_id import fetch_user_id
from ...utils.twitter_db_operation import retrieve_user_creds

from ...services.twitter import service_twitter_login


BEARER_TOKEN = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'


def calculate_iterations_required(output_count):
    base_iterations = math.floor(output_count / 20)
    last_iteration_output_count = output_count%20

    return base_iterations,last_iteration_output_count

def convert_date(date_string):
    # Parse the date string
    parsed_date = datetime.strptime(date_string, '%a %b %d %H:%M:%S %z %Y')

    # Convert the parsed date to local time
    local_time = parsed_date.astimezone()

    # Format the local time as required
    formatted_date = local_time.strftime('%Y-%m-%d %H:%M:%S')

    return formatted_date


def process_search_results(session, search_string, iterations_count, last_iteration_output_count, x_csrf_token):
    final_output_data = []
    run_without_cursor_param = True
    display_count = 0
    final_result_count = 0

    while iterations_count > 0:
        logger.info(f"Searching for {display_count}th iteration")
        
        iterations_count -= 1
        
        try:
            if run_without_cursor_param:
                url = f"https://twitter.com/i/api/graphql/ummoVKaeoT01eUyXutiSVQ/SearchTimeline?variables=%7B%22rawQuery%22%3A%22{search_string}%22%2C%22count%22%3A20%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Latest%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
                run_without_cursor_param = False
            else:
                url = f"https://twitter.com/i/api/graphql/ummoVKaeoT01eUyXutiSVQ/SearchTimeline?variables=%7B%22rawQuery%22%3A%22{search_string}%22%2C%22count%22%3A20%2C%22cursor%22%3A%22{cursor_value}%22%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Latest%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
                
            search_result, cursor_value, result_count= fetch_search_result(session, url, search_string, x_csrf_token, display_count)
            final_result_count+= result_count
            final_output_data.append(search_result) if len(search_result) > 0 else None
            display_count += 1
        except Exception as e:
            logger.error(f"Error fetching search result: {e}")
            return final_output_data, final_result_count

    if last_iteration_output_count > 0:
        try:
            logger.info(f"Searching for {display_count}th iteration in extra iteration")
            
            if (display_count > 0):
                url = f"https://twitter.com/i/api/graphql/ummoVKaeoT01eUyXutiSVQ/SearchTimeline?variables=%7B%22rawQuery%22%3A%22{search_string}%22%2C%22count%22%3A{last_iteration_output_count}%2C%22cursor%22%3A%22{cursor_value}%22%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Latest%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
            else:
                url = f"https://twitter.com/i/api/graphql/ummoVKaeoT01eUyXutiSVQ/SearchTimeline?variables=%7B%22rawQuery%22%3A%22{search_string}%22%2C%22count%22%3A{last_iteration_output_count}%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Latest%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
            
            search_result, cursor_value, result_count = fetch_search_result(session, url, search_string, x_csrf_token, display_count)
            final_result_count+= result_count
            final_output_data.append(search_result) if len(search_result) > 0 else None
        except Exception as e:
            logger.error(f"Error fetching extra iteration search result: {e}")
            return final_output_data, final_result_count


    return final_output_data, final_result_count

    

def fetch_search_result(session, url, search_string, x_csrf_token, display_count):
    logger.info(f"**generating search result for the given string: {search_string}")

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
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://twitter.com/search?q=modi&src=typed_query',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Priority': 'u=1, i',
    }

    try:
        response = session.get(url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        json_response = response.json()

        # Extract tweet_collection and cursor_value_tweet_collection
        tweet_collection = json_response.get("data", {}).get("search_by_raw_query", {}).get("search_timeline", {}).get("timeline", {}).get("instructions", [])[0].get("entries", [])
        cursor_value_tweet_collection = tweet_collection

        if display_count >= 1:
            cursor_value_tweet_collection = json_response.get("data", {}).get("search_by_raw_query", {}).get("search_timeline", {}).get("timeline", {}).get("instructions", [])[2]

        # Process search result and cursor value
        search_result, result_count = clean_search_result(tweet_collection=tweet_collection)
        cursor_value = fetch_cursor_value(tweet_collection=cursor_value_tweet_collection, display_count=display_count)

        return search_result, cursor_value, result_count

    except requests.RequestException as e:
        logger.error(f"Error fetching search result: {e}")
        return None, None, None  # Return None for all values if an error occurs
    except (KeyError, IndexError) as e:
        logger.error(f"Error parsing JSON response: {e}")
        return None, None, None  # Return None for all values if JSON parsing error occurs


def process_personal_info(user_info):
    # Initialize default values
    legacy_user_info = user_info.get("legacy", {})
    sourceAccountName = legacy_user_info.get("name", "N.A")
    sourceAccountUsername = legacy_user_info.get("screen_name", "N.A")
    sourceFollowerCount = legacy_user_info.get("followers_count", "N.A")
    sourceFollowingCount = legacy_user_info.get("friends_count", "N.A")

    # Construct dictionary containing processed user information
    sourceUserInfo = {
        "sourceAccountName": sourceAccountName,
        "sourceAccountUsername": sourceAccountUsername,
        "sourceFollowerCount": sourceFollowerCount,
        "sourceFollowingCount": sourceFollowingCount
    }

    return sourceUserInfo


def process_tweet_info(tweet_info):
    # Initialize default values
    sourceTweetCreationTime = tweet_info.get("created_at", "N.A")
    sourceLikeCount = tweet_info.get("favorite_count", "N.A")
    sourceTextContent = tweet_info.get("full_text", "N.A")
    sourceCommentCount = tweet_info.get("reply_count", "N.A")
    sourceRetweetCount = tweet_info.get("retweet_count", "N.A")
    sourceHashtags = []
    sourceMediaContent = []

    # Extract hashtags if available
    hashtags = tweet_info.get("entities", {}).get("hashtags", [])
    for hashtag in hashtags:
        text_content = hashtag.get("text", "")
        if text_content:
            sourceHashtags.append(f"#{text_content}")

    # Extract media content if available
    media_contents = tweet_info.get("entities", {}).get("media", [])
    for media_content in media_contents:
        media_content_type = media_content.get("type", "")
        if media_content_type == "photo":
            sourceMediaContent.append(media_content.get("media_url_https", ""))
        elif media_content_type == "video":
            video_info_variants = media_content.get("video_info", {}).get("variants", [])
            for video_info in video_info_variants:
                if video_info.get("content_type", "") == "video/mp4":
                    sourceMediaContent.append(video_info.get("url", ""))

    # Construct dictionary containing processed tweet information
    sourceOrganicTweetDetail = {
        "sourceTweetCreationTime": convert_date(sourceTweetCreationTime),
        "sourceLikeCount": sourceLikeCount,
        "sourceTextContent": sourceTextContent,
        "sourceCommentCount": sourceCommentCount,
        "sourceRetweetCount": sourceRetweetCount,
        "sourceHashtags": sourceHashtags,
        "sourceMediaContent": sourceMediaContent
    }

    return sourceOrganicTweetDetail

            
    

def clean_search_result(tweet_collection):
    search_results = []
    result_count = 0

    for tweet in tweet_collection:
        single_search_result = {}

        # Extract entryId of the tweet
        entry_id = tweet.get("entryId")

        # Check if entryId starts with "tweet"
        if str(entry_id).startswith("tweet"):
            core_result = tweet.get("content", {}).get("itemContent", {}).get("tweet_results", {}).get("result", {})

            # If "tweet" key exists in core_result, update core_result to its value
            if "tweet" in core_result:
                core_result = core_result["tweet"]

            # Extract user info and tweet info from core_result
            user_info = core_result.get("core", {}).get("user_results", {}).get("result", {})
            tweet_info = core_result.get("legacy", {})

            # Process user info and tweet info
            source_user_info = process_personal_info(user_info=user_info)
            source_user_info["isSourceXVerified"] = user_info.get("is_blue_verified", "N.A")
            source_organic_tweet_detail = process_tweet_info(tweet_info=tweet_info)
            source_organic_tweet_detail["sourceEngagementCount"] = core_result.get("views", {}).get("count", "N.A")

            # Populate single search result with processed information
            single_search_result["sourceUserInfo"] = source_user_info
            single_search_result["sourceOrganicTweetDetail"] = source_organic_tweet_detail
            result_count+= 1

            # Append single search result to search results list
            search_results.append(single_search_result)

    return search_results, result_count


def fetch_cursor_value(tweet_collection, display_count):
    # Check if display_count is greater than or equal to 1
    if display_count >= 1:
        # Get replacement_entry_id from tweet_collection, defaulting to "N.A" if not found
        replacement_entry_id = tweet_collection.get("entry_id_to_replace", "N.A")
        
        # Check if replacement_entry_id is "cursor-bottom-0"
        if str(replacement_entry_id) == "cursor-bottom-0":
            # Get cursor_value from tweet_collection and return it
            cursor_value = tweet_collection.get("entry", {}).get("content", {}).get("value")
            return cursor_value
    else:
        # Loop through tweet_collection in reverse order
        for tweet in reversed(tweet_collection):
            entry_id = tweet["entryId"]
            
            # Check if entry_id is "cursor-bottom-0"
            if str(entry_id) == "cursor-bottom-0":
                # Get cursor_value from tweet and log it
                cursor_value = tweet.get("content", {}).get("value")
                return cursor_value


def test_func(session, x_csrf_token, user_id, username):

    url = f"https://twitter.com/i/api/graphql/WmvfySbQ0FeY1zk4HU_5ow/UserTweets?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22count%22%3A20%2C%22includePromotedContent%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"

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
    'Priority': 'u=1, i'
    }

    response = session.get(url, headers=headers, data=payload)

    return json.loads(response.text)




def driver_function(data):
    logger.info(f"Hitting the driver function")

    

    search_string = str(data.query_string).strip()
    output_count = data.query_length
    session, x_csrf_token = service_twitter_login.driver_function()

    base_iterations,last_iteration_output_count = calculate_iterations_required(output_count = output_count)
    
    logger.info(f"going forward with base iteration {base_iterations} & last iteration output count {last_iteration_output_count}")

    user_id = fetch_user_id(session, x_csrf_token, search_string)

    # final_output_data, final_result_count =  process_search_results(session, search_string, base_iterations, last_iteration_output_count, x_csrf_token)

    # search_result_count = {
    #     "resultCount": final_result_count
    # }

    # final_output_data.insert(0, search_result_count)

    # return final_output_data

    return test_func(session, x_csrf_token, user_id, search_string)
    


# driver_function("prithidevghosh","Ghosh@39039820")
