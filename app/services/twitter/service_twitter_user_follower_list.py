import requests
import json
import math
from datetime import datetime


from ...utils.logger import logger
from ...utils.fetch_user_id import fetch_user_id

from ...services.twitter import service_twitter_login


BEARER_TOKEN = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
SERVICE_NAME = 'TWITTER-USER-FOLLOWER-LIST'
VERIFIED_FOLLOWER_REFERER = ""
NON_VERIFIED_FOLLOWER_REFERER = ""


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

def url_dispenser(user_id, verification_filter, last_iteration_output_count = None, cursor_value = None):
    if verification_filter:
        if cursor_value is not None:
            if last_iteration_output_count is not None:
                return f"https://twitter.com/i/api/graphql/XzDD4ocymM4tBqKql_nfWw/BlueVerifiedFollowers?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22count%22%3A{last_iteration_output_count}%2C%22cursor%22%3A%22{cursor_value}%22%2C%22includePromotedContent%22%3Afalse%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
            elif last_iteration_output_count is None:
                return f"https://twitter.com/i/api/graphql/XzDD4ocymM4tBqKql_nfWw/BlueVerifiedFollowers?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22count%22%3A20%2C%22cursor%22%3A%22{cursor_value}%22%2C%22includePromotedContent%22%3Afalse%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
        elif cursor_value is None:
            if last_iteration_output_count is not None:
                return f"https://twitter.com/i/api/graphql/XzDD4ocymM4tBqKql_nfWw/BlueVerifiedFollowers?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22count%22%3A{last_iteration_output_count}%2C%22includePromotedContent%22%3Afalse%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
            elif last_iteration_output_count is None:
                return f"https://twitter.com/i/api/graphql/XzDD4ocymM4tBqKql_nfWw/BlueVerifiedFollowers?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22count%22%3A20%2C%22includePromotedContent%22%3Afalse%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
    else:
        if cursor_value is not None:
            if last_iteration_output_count is not None:
                return f"https://twitter.com/i/api/graphql/SAuX47ZqVkz9Y-4gEsdp0A/Followers?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22count%22%3A{last_iteration_output_count}%2C%22cursor%22%3A%22{cursor_value}%22%2C%22includePromotedContent%22%3Afalse%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
            elif last_iteration_output_count is None:
                return f"https://twitter.com/i/api/graphql/SAuX47ZqVkz9Y-4gEsdp0A/Followers?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22count%22%3A20%2C%22cursor%22%3A%22{cursor_value}%22%2C%22includePromotedContent%22%3Afalse%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
        elif cursor_value is None:
            if last_iteration_output_count is not None:
                return f"https://twitter.com/i/api/graphql/SAuX47ZqVkz9Y-4gEsdp0A/Followers?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22count%22%3A{last_iteration_output_count}%2C%22includePromotedContent%22%3Afalse%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
            elif last_iteration_output_count is None:
                return f"https://twitter.com/i/api/graphql/SAuX47ZqVkz9Y-4gEsdp0A/Followers?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22count%22%3A20%2C%22includePromotedContent%22%3Afalse%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"




def process_search_results(session, verification_filter, user_id, username, iterations_count, last_iteration_output_count, x_csrf_token, output_count):
    logger.info(f"***{SERVICE_NAME}::: processing search result for the given username: {username}")
    final_output_data = []
    run_without_cursor_param = True
    display_count = 0
    final_result_count = 0

    while iterations_count > 0:
        logger.info(f"***{SERVICE_NAME}::: Searching for {display_count}th iteration")
        
        iterations_count -= 1
        
        try:
            if run_without_cursor_param:
                url = url_dispenser(user_id, verification_filter, None, None)
                run_without_cursor_param = False
            else:
                url = url_dispenser(user_id, verification_filter, None, cursor_value)

            search_result, cursor_value, result_count= fetch_search_result(session, verification_filter, url, user_id, username, x_csrf_token, display_count)
            final_result_count+= result_count
            final_output_data.append(search_result) if len(search_result) > 0 else None
            if final_result_count >= output_count:
                return final_output_data, final_result_count
            display_count += 1
        except Exception as e:
            logger.error(f"Error fetching search result: {e}")
            return final_output_data, final_result_count

    if last_iteration_output_count > 0:
        try:
            logger.info(f"Searching for {display_count}th iteration in extra iteration")
            
            if (display_count > 0):
                url = url_dispenser(user_id, verification_filter, last_iteration_output_count, cursor_value)
            else:
                url = url_dispenser(user_id, verification_filter, last_iteration_output_count, None)

            search_result, cursor_value, result_count = fetch_search_result(session, verification_filter, url, user_id, username, x_csrf_token, display_count)
            final_result_count+= result_count
            final_output_data.append(search_result) if len(search_result) > 0 else None
            if final_result_count >= output_count:
                return final_output_data, final_result_count
        except Exception as e:
            logger.error(f"Error fetching extra iteration search result: {e}")
            return final_output_data, final_result_count


    return final_output_data, final_result_count



def fetch_search_result(session, verification_filter, url, user_id, username, x_csrf_token, display_count):

    logger.info(f"***{SERVICE_NAME}::: generating search result for the given username: {username}")
    
    if verification_filter:
        referer_url = f'https://twitter.com/{username}/verified_followers'
    else:
        referer_url = f'https://twitter.com/{username}/followers'
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
        'Referer': referer_url,
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Priority': 'u=1, i'
    }

    try:
        response = session.get(url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        json_response = response.json()

        # Extract tweet_collection and cursor_value_tweet_collection
        following_collection = json_response.get("data", {}).get("user", {}).get("result", {}).get("timeline", {}).get("timeline", {}).get("instructions", [])
    
        for following in following_collection:
            if following.get("type") == "TimelineAddEntries":
                following_collection_entries = following.get("entries")
                break

        
        # Process search result and cursor value
        search_result, result_count = clean_search_result(following_collection = following_collection_entries)
        cursor_value = fetch_cursor_value(following_collection_entries = following_collection_entries)

        return search_result, cursor_value, result_count

    except requests.RequestException as e:
        logger.error(f"Error fetching search result: {e}")
        return None, None, None  # Return None for all values if an error occurs
    except (KeyError, IndexError) as e:
        logger.error(f"Error parsing JSON response: {e}")
        return None, None, None  # Return None for all values if JSON parsing error occurs


def process_personal_info(user_info):
    logger.info(f"***{SERVICE_NAME}::: processing user personal info")
    # Initialize default values
    legacy_user_info = user_info.get("legacy", {})
    sourceAccountName = legacy_user_info.get("name", "N.A")
    sourceAccountUsername = legacy_user_info.get("screen_name", "N.A")
    sourceFollowerCount = legacy_user_info.get("followers_count", "N.A")
    sourceFollowingCount = legacy_user_info.get("friends_count", "N.A")
    sourceProfileImage = legacy_user_info.get("profile_image_url_https", "N.A")
    sourceProfileBanner = legacy_user_info.get("profile_banner_url", "N.A")

    # Construct dictionary containing processed user information
    sourceUserInfo = {
        "sourceAccountName": sourceAccountName,
        "sourceAccountUsername": sourceAccountUsername,
        "sourceFollowerCount": sourceFollowerCount,
        "sourceFollowingCount": sourceFollowingCount,
        "sourceProfileImage": sourceProfileImage,
        "sourceProfileBanner": sourceProfileBanner
    }

    return sourceUserInfo

            
    

def clean_search_result(following_collection):
    logger.info(f"***{SERVICE_NAME}::: cleaning search results")
    search_results = []
    result_count = 0

    for follow in following_collection:
        single_search_result = {}

        # Extract entryId of the tweet
        entry_id = follow.get("entryId")

        # Check if entryId starts with "tweet"
        if str(entry_id).startswith("user"):
            core_result = follow.get("content", {}).get("itemContent", {}).get("user_results", {}).get("result", {})


            # Extract user info and tweet info from core_result
            # user_info = core_result.get("core", {}).get("user_results", {}).get("result", {})
            # tweet_info = core_result.get("legacy", {})

            # Process user info and tweet info
            source_user_info = process_personal_info(user_info = core_result)
            source_user_info["isSourceXVerified"] = core_result.get("is_blue_verified", "N.A")

            # Populate single search result with processed information
            single_search_result["sourceUserInfo"] = source_user_info
            result_count+= 1

            # Append single search result to search results list
            search_results.append(single_search_result)

    return search_results, result_count


def fetch_cursor_value(following_collection_entries):
    logger.info(f"***{SERVICE_NAME}::: fetching cursor value")
    
    for entry in reversed(following_collection_entries):
            if entry.get("entryId").startswith("cursor-bottom"):
                cursor_value = entry.get("content").get("value")
                return cursor_value




def driver_function(data):
    logger.info(f"***Hitting the driver function of service: {SERVICE_NAME}")

    

    search_string = str(data.query_string).strip()
    output_count = data.query_length
    verification_filter = data.verification_filter

    session, x_csrf_token = service_twitter_login.driver_function()

    base_iterations,last_iteration_output_count = calculate_iterations_required(output_count = output_count)
    
    logger.info(f"***going forward with base iteration {base_iterations} & last iteration output count {last_iteration_output_count}")

    # return fetch_search_result(session=session,search_string=search_string, output_count=output_count, x_csrf_token=x_csrf_token)
    user_id = fetch_user_id(session, x_csrf_token, search_string)

 
    final_output_data, final_result_count =  process_search_results(session, verification_filter, user_id, search_string, base_iterations, last_iteration_output_count, x_csrf_token, output_count)
  
    

    search_result_count = {
        "resultCount": final_result_count
    }

    final_output_data.insert(0, search_result_count)

    return final_output_data
    


# driver_function("prithidevghosh","Ghosh@39039820")
