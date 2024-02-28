import requests
import json
import math


from ...utils.logger import logger
# from fastapi.logger import logger
from ...utils.twitter_db_operation import retrieve_user_creds



BEARER_TOKEN = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
SERVICE_NAME = "TWITTER-LOGIN-PROCESSOR"

def create_session():
    logger.info(f"***{SERVICE_NAME}::: creating new session")
    session = requests.Session()
    return session

def generate_headers(session):
    logger.info(f"***{SERVICE_NAME}::: generating headers")
    url = "https://api.twitter.com/1.1/guest/activate.json"
    bearer_token = BEARER_TOKEN

    response = session.post(url, headers={"Authorization": f"{bearer_token}"})
    json_data = response.json()

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "X-Guest-Token": json_data["guest_token"]
    }

    return headers["X-Guest-Token"]


def get_initial_flow_token(session, x_guest_token):

    logger.info(f"***{SERVICE_NAME}::: generating initial flow tokens")

    url = "https://api.twitter.com/1.1/onboarding/task.json?flow_name=login"

    payload = json.dumps({
    "input_flow_data": {
        "flow_context": {
        "debug_overrides": {},
        "start_location": {
            "location": "splash_screen"
        }
        }
    },
    "subtask_versions": {
        "action_list": 2,
        "alert_dialog": 1,
        "app_download_cta": 1,
        "check_logged_in_account": 1,
        "choice_selection": 3,
        "contacts_live_sync_permission_prompt": 0,
        "cta": 7,
        "email_verification": 2,
        "end_flow": 1,
        "enter_date": 1,
        "enter_email": 2,
        "enter_password": 5,
        "enter_phone": 2,
        "enter_recaptcha": 1,
        "enter_text": 5,
        "enter_username": 2,
        "generic_urt": 3,
        "in_app_notification": 1,
        "interest_picker": 3,
        "js_instrumentation": 1,
        "menu_dialog": 1,
        "notifications_permission_prompt": 2,
        "open_account": 2,
        "open_home_timeline": 1,
        "open_link": 1,
        "phone_verification": 4,
        "privacy_options": 1,
        "security_key": 3,
        "select_avatar": 4,
        "select_banner": 2,
        "settings_list": 7,
        "show_code": 1,
        "sign_up": 2,
        "sign_up_review": 4,
        "tweet_selection_urt": 1,
        "update_users": 1,
        "upload_media": 1,
        "user_recommendations_list": 4,
        "user_recommendations_urt": 1,
        "wait_spinner": 3,
        "web_modal": 1
    }
    })
    headers = {
    'Host': 'api.twitter.com',
    'Content-Length': '930',
    'Sec-Ch-Ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
    'X-Twitter-Client-Language': 'en-GB',
    'Sec-Ch-Ua-Mobile': '?0',
    'Authorization': f"{BEARER_TOKEN}",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.199 Safari/537.36',
    'Content-Type': 'application/json',
    'X-Guest-Token': x_guest_token,
    'X-Twitter-Active-User': 'yes',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Accept': '*/*',
    'Origin': 'https://twitter.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://twitter.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Priority': 'u=1, i',
    }

    response = session.post(url, headers=headers, data=payload)

    json_response =  json.loads(response.text)

    flow_token_v0 = json_response['flow_token']

    url = "https://api.twitter.com/1.1/onboarding/task.json"

    payload = json.dumps({
    "flow_token": f"{flow_token_v0}",
    "subtask_inputs": [
        {
        "subtask_id": "LoginJsInstrumentationSubtask",
        "js_instrumentation": {
            "response": "{}",
            "link": "next_link"
        }
        }
    ]
    })
    headers = {
    'Host': 'api.twitter.com',
    'Content-Length': '864',
    'Sec-Ch-Ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
    'X-Twitter-Client-Language': 'en-GB',
    'Sec-Ch-Ua-Mobile': '?0',
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.199 Safari/537.36',
    'Content-Type': 'application/json',
    'X-Client-Transaction-Id': '/Rl/Z+BkZYKe53UHc2IZGlbbTuHY5t55QRheotcSo2vA9q/2bO5g1gzUQ3VKr57vtLw8efwVMcElxOpKM57ghdGLo1Cb/A',
    'X-Guest-Token': f"{x_guest_token}",
    'X-Twitter-Active-User': 'yes',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Accept': '*/*',
    'Origin': 'https://twitter.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://twitter.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Priority': 'u=1, i',
    # 'Cookie': 'att=1-YJwdKtzxej0lHd5bPFKXSulKk6gagrz4KVDnl4o9; guest_id=v1%3A170840112949626105; guest_id_ads=v1%3A170840112949626105; guest_id_marketing=v1%3A170840112949626105; personalization_id="v1_o/fcwFGx0qIrz2cb/zj5zg=="'
    }

    response = session.post(url, headers=headers, data=payload)

    json_response =  json.loads(response.text)

    flow_token_v1 = json_response['flow_token']

    return flow_token_v1

def process_login(session, flow_token_v1, username, user_password, x_guest_token):
    logger.info(f"***{SERVICE_NAME}::: processing login with creds: {username, user_password}")

    url = "https://api.twitter.com/1.1/onboarding/task.json"

    payload = json.dumps({
    "flow_token": flow_token_v1,
    "subtask_inputs": [
        {
        "subtask_id": "LoginEnterUserIdentifierSSO",
        "settings_list": {
            "setting_responses": [
            {
                "key": "user_identifier",
                "response_data": {
                "text_data": {
                    "result": username
                }
                }
            }
            ],
            "link": "next_link"
        }
        }
    ]
    })
    headers = {
    'Host': 'api.twitter.com',
    'Content-Length': '296',
    'Sec-Ch-Ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
    'X-Twitter-Client-Language': 'en-GB',
    'Sec-Ch-Ua-Mobile': '?0',
    'Authorization': f'{BEARER_TOKEN}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.199 Safari/537.36',
    'Content-Type': 'application/json',
    'X-Guest-Token': f'{x_guest_token}',
    'X-Twitter-Active-User': 'yes',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Accept': '*/*',
    'Origin': 'https://twitter.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://twitter.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Priority': 'u=1, i',
    }

    response = session.post(url, headers=headers, data=payload)

    json_response =  json.loads(response.text)

    flow_token_v2 = json_response['flow_token']

    url = "https://api.twitter.com/1.1/onboarding/task.json"

    payload = json.dumps({
    "flow_token": flow_token_v2,
    "subtask_inputs": [
        {
        "subtask_id": "LoginEnterPassword",
        "enter_password": {
            "password": user_password,
            "link": "next_link"
        }
        }
    ]
    })
    headers = {
    'Host': 'api.twitter.com',
    'Content-Length': '200',
    'Sec-Ch-Ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
    'X-Twitter-Client-Language': 'en-GB',
    'Sec-Ch-Ua-Mobile': '?0',
    'Authorization': f'{BEARER_TOKEN}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.199 Safari/537.36',
    'Content-Type': 'application/json',
    'X-Guest-Token': f'{x_guest_token}',
    'X-Twitter-Active-User': 'yes',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Accept': '*/*',
    'Origin': 'https://twitter.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://twitter.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Priority': 'u=1, i'
    }

    response = session.post(url, headers=headers, data=payload)

    json_response =  json.loads(response.text)

    flow_token_v3 = json_response['flow_token']

    return flow_token_v3

def generate_x_csrf_token(session, flow_token_v3, x_guest_token):
    logger.info(f"***{SERVICE_NAME}::: generating x-csrf-token")

    url = "https://api.twitter.com/1.1/onboarding/task.json"

    payload = json.dumps({
    "flow_token": flow_token_v3,
    "subtask_inputs": [
        {
        "subtask_id": "AccountDuplicationCheck",
        "check_logged_in_account": {
            "link": "AccountDuplicationCheck_false"
        }
        }
    ]
    })
    headers = {
    'Host': 'api.twitter.com',
    'Content-Length': '206',
    'Sec-Ch-Ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
    'X-Twitter-Client-Language': 'en-GB',
    'Sec-Ch-Ua-Mobile': '?0',
    'Authorization': f'{BEARER_TOKEN}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.199 Safari/537.36',
    'Content-Type': 'application/json',
    'X-Guest-Token': f'{x_guest_token}',
    'X-Twitter-Active-User': 'yes',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Accept': '*/*',
    'Origin': 'https://twitter.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://twitter.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Priority': 'u=1, i',
    }

    response = session.post(url, headers=headers, data=payload)

    cookies = response.cookies
    cookie_jar={}
 
    for cookie in cookies:
        cookie_jar[cookie.name]=cookie.value
    
    x_csrf_token = cookie_jar["ct0"]
    auth_token = cookie_jar["auth_token"]


    url = "https://api.twitter.com/graphql/W62NnYgkgziw9bwyoVht0g/Viewer?variables=%7B%22withCommunitiesMemberships%22%3Atrue%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D&fieldToggles=%7B%22isDelegate%22%3Afalse%2C%22withAuxiliaryUserLabels%22%3Afalse%7D"

    payload = {}
    headers = {
    'Host': 'api.twitter.com',
    'Sec-Ch-Ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
    'X-Twitter-Client-Language': 'en-GB',
    'X-Csrf-Token': f'{x_csrf_token}',
    'Sec-Ch-Ua-Mobile': '?0',
    'Authorization': f'{BEARER_TOKEN}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.199 Safari/537.36',
    'Content-Type': 'application/json',
    'X-Guest-Token': f'{x_guest_token}',
    'X-Twitter-Active-User': 'yes',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Accept': '*/*',
    'Origin': 'https://twitter.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://twitter.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Priority': 'u=1, i',
    }

    response = session.get(url, headers=headers, data=payload)
    # print(response.text)


    cookies = response.cookies
 
    for cookie in cookies:
        cookie_jar[cookie.name]=cookie.value

    x_csrf_token = cookie_jar["ct0"]

    return x_csrf_token




def driver_function():
    logger.info(f"***Hitting the driver function of service: {SERVICE_NAME}")

    login_creds = retrieve_user_creds(service_name = "twitter")
    username = login_creds["username"]
    password = login_creds["password"]


    session = create_session()

    # base_iterations,last_iteration_output_count = calculate_iterations_required(output_count = output_count)
    
    # logger.info(f"going forward with base iteration {base_iterations} & last iteration output count {last_iteration_output_count}")
    
    x_guest_token = generate_headers(session=session)
    # print(x_guest_token)

    flow_token_v1 = get_initial_flow_token(session=session,x_guest_token=x_guest_token)
    # print(flow_token_v1)

    flow_token_v3 = process_login(session=session,flow_token_v1=flow_token_v1,username=username, user_password=password,x_guest_token=x_guest_token)

    # print(flow_token_v3)
    x_csrf_token = generate_x_csrf_token(session=session,flow_token_v3=flow_token_v3,x_guest_token=x_guest_token)
    # print(x_csrf_token)

    # return fetch_search_result(session=session,search_string=search_string, output_count=output_count, x_csrf_token=x_csrf_token)

    return session, x_csrf_token




# driver_function("prithidevghosh","Ghosh@39039820")
