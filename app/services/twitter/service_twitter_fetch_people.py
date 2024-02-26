import math
import json
from ...services.twitter import service_twitter_login
from ...utils.logger import logger

BEARER_TOKEN = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'


def calculate_iterations_required(output_count):
    base_iterations = math.floor(output_count / 20)
    last_iteration_output_count = output_count%20

    return base_iterations,last_iteration_output_count




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
                url = f"https://twitter.com/i/api/graphql/ummoVKaeoT01eUyXutiSVQ/SearchTimeline?variables=%7B%22rawQuery%22%3A%22{search_string}%22%2C%22count%22%3A20%2C%22querySource%22%3A%22recent_search_click%22%2C%22product%22%3A%22People%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
                run_without_cursor_param = False
            else:
                url = f"https://twitter.com/i/api/graphql/ummoVKaeoT01eUyXutiSVQ/SearchTimeline?variables=%7B%22rawQuery%22%3A%22{search_string}%22%2C%22count%22%3A20%2C%22cursor%22%3A%22{cursor_value}%22%2C%22querySource%22%3A%22recent_search_click%22%2C%22product%22%3A%22People%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
                
            search_result, cursor_value, result_count= fetch_people_list(session, url, search_string, x_csrf_token, display_count)
            final_result_count+= result_count
            final_output_data.append(search_result) if len(search_result) > 0 else None
            display_count += 1
        except Exception as e:
            logger.error(f"Error fetching people list: {e}")
            return final_output_data, final_result_count

    if last_iteration_output_count > 0:
        try:
            logger.info(f"Searching for {display_count}th iteration in extra iteration")
            print(cursor_value)
            
            if (display_count > 0):
                print("entering in 1")
                url = f"https://twitter.com/i/api/graphql/ummoVKaeoT01eUyXutiSVQ/SearchTimeline?variables=%7B%22rawQuery%22%3A%22{search_string}%22%2C%22count%22%3A{last_iteration_output_count}%2C%22cursor%22%3A%22{cursor_value}%22%2C%22querySource%22%3A%22recent_search_click%22%2C%22product%22%3A%22People%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
            else:
                print("entering in 2")
                url = f"https://twitter.com/i/api/graphql/ummoVKaeoT01eUyXutiSVQ/SearchTimeline?variables=%7B%22rawQuery%22%3A%22{search_string}%22%2C%22count%22%3A{last_iteration_output_count}%2C%22querySource%22%3A%22recent_search_click%22%2C%22product%22%3A%22People%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
            
            search_result, cursor_value, result_count = fetch_people_list(session, url, search_string, x_csrf_token, display_count)
            final_result_count+= result_count
            final_output_data.append(search_result) if len(search_result) > 0 else None
        except Exception as e:
            logger.error(f"Error fetching extra iteration search result: {e}")
            return final_output_data, final_result_count
    
    

    return final_output_data, final_result_count

def fetch_people_list(session, url, search_string, x_csrf_token, display_count):

    # url = f"https://twitter.com/i/api/graphql/ummoVKaeoT01eUyXutiSVQ/SearchTimeline?variables=%7B%22rawQuery%22%3A%22{search_string}%22%2C%22count%22%3A20%2C%22querySource%22%3A%22recent_search_click%22%2C%22product%22%3A%22People%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"

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
    'Referer': f'https://twitter.com/search?q={search_string}&src=recent_search_click&f=user',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Priority': 'u=1, i'
    }

    response = session.get(url, headers=headers, data=payload)

    json_response = response.json()

    # Extract tweet_collection and cursor_value_tweet_collection
    
    if display_count >= 1:
        user_collection = json_response.get("data", {}).get("search_by_raw_query", {}).get("search_timeline", {}).get("timeline", {}).get("instructions", [])[0].get("entries", [])
    else:
        user_collection = json_response.get("data", {}).get("search_by_raw_query", {}).get("search_timeline", {}).get("timeline", {}).get("instructions", [])[1].get("entries", [])

    cursor_value = fetch_cursor_value(user_collection)
    search_result, result_count = clean_search_result(user_collection)


    return search_result, cursor_value, result_count



    



def process_personal_info(user_info):
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

            
    

def clean_search_result(user_collection):
    search_results = []
    result_count = 0

    for user in user_collection:
        single_search_result = {}

        # Extract entryId of the tweet
        entry_id = user.get("entryId")

        # Check if entryId starts with "tweet"
        if str(entry_id).startswith("user"):
            core_result = user.get("content", {}).get("itemContent", {}).get("user_results", {}).get("result", {})
 

            # Process user info and tweet info
            source_user_info = process_personal_info(user_info=core_result)
            source_user_info["isSourceXVerified"] = core_result.get("is_blue_verified", "N.A")

            # Populate single search result with processed information
            single_search_result["sourceUserInfo"] = source_user_info
            result_count+=1
     

            # Append single search result to search results list
            search_results.append(single_search_result)

    return search_results,result_count


def fetch_cursor_value(user_collection):
    # Check if display_count is greater than or equal to 1
    for tweet in reversed(user_collection):
        entry_id = tweet["entryId"]
        
        # Check if entry_id is "cursor-bottom-0"
        if str(entry_id).startswith("cursor-bottom"):
            # Get cursor_value from tweet and log it
            cursor_value = tweet.get("content", {}).get("value")
            return cursor_value


def driver_function(data):
    search_string = str(data.query_string).strip()
    output_count = data.query_length
    session, x_csrf_token = service_twitter_login.driver_function()

    base_iterations,last_iteration_output_count = calculate_iterations_required(output_count = output_count)
    
    logger.info(f"going forward with base iteration {base_iterations} & last iteration output count {last_iteration_output_count}")

    
    final_output_data, final_result_count = process_search_results(session, search_string, base_iterations, last_iteration_output_count, x_csrf_token)
    
    search_result_count = {
        "resultCount": final_result_count
    }

    final_output_data.insert(0, search_result_count)

    return final_output_data