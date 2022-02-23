import requests
import os
import json
from dotenv import load_dotenv
import pathlib

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

# name the file we want
env_file_name = 'lrhf97_twit_cred.env'
curr_file = pathlib.Path(__file__).parent
env_path = curr_file.joinpath(env_file_name)

load_dotenv(env_path)

bearer_token = os.getenv("BEARER_TOKEN")


def create_url(max_results=50):
    user_id = 3413455348
    search_url = "https://api.twitter.com/2/users/{}/followers?max_results={}".format(user_id,max_results)

    params ={'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'next_token': {}}
    return (search_url, params)


def bearer_oauth(r):

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r


def connect_to_endpoint(url, params, next_token=None):
    params['pagination_token'] = next_token # param object recieved form the create_url function
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()