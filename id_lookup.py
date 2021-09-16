
import requests
import os
import json
from dotenv import load_dotenv
import pathlib

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

# name the file we want
env_file_name = 'lrhf97_twit_cred.env'

# designate the path of the file
curr_file = pathlib.Path(__file__).parent

# join them
env_path = curr_file.joinpath(env_file_name)

# load the file
load_dotenv(env_path)


bearer_token = os.getenv("BEARER_TOKEN")

def create_url():
    # Replace with username
    # user_id = 15903747
    username = 'ridgesupply'

    # https://api.twitter.com/2/users/by?usernames=TwitterDev,Twitter

    return "https://api.twitter.com/2/users/by?usernames={}".format(username)

def get_params():
    return {"user.fields":"id",
            "user.fields":"description"}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    url = create_url()
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main() 


