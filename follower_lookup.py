import requests
import os
import json
from dotenv import load_dotenv
import pathlib
import csv
import dateutil.parser
import pandas as pd
import time



# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

# name the file we want
env_file_name = 'lrhf97_twit_cred.env'
curr_file = pathlib.Path(__file__).parent
env_path = curr_file.joinpath(env_file_name)

load_dotenv(env_path)

bearer_token = os.getenv("BEARER_TOKEN")

csv_to_file = "data/rs_fr_list.csv"
ridge_supply_id = 3413455348

def create_url(user_id,max_results=50):
    # user_id = 3413455348
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


url = create_url(user_id = ridge_supply_id,max_results=50)
json_response = connect_to_endpoint(url[0], url[1], next_token=None)

csvFile = open(csv_to_file, "a", newline="", encoding='utf-8')
csvWriter = csv.writer(csvFile)

#Create headers for the data you want to save, in this example, we only want save these columns in our dataset
csvWriter.writerow(['id', 'created_at', 'location', 'description','username','name','verified', 'followers_count', 'following_count', 'tweet_count','listed_count'])
csvFile.close()

def append_to_csv(json_response, fileName):

    #A counter variable
    counter = 0

    #Open OR create the target CSV file
    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Loop through each tweet
    for tweet in json_response['data']:
        
        # We will create a variable for each since some of the keys might not exist for some tweets
        # So we will account for that

        # 1. ID
        id = tweet['id']

        # 2. Time created
        created_at = dateutil.parser.parse(tweet['created_at'])

        # 3. location
        if ('location' in tweet):   
            location = tweet['location']
        else:
            location = " "

        # 4. description
        description = tweet['description']

        # # 5. names
        username = tweet['username']
        name = tweet['name']
        verified = tweet['verified']

        # 6. Tweet metrics
        followers_count = tweet['public_metrics']['followers_count']
        following_count = tweet['public_metrics']['following_count']
        tweet_count = tweet['public_metrics']['tweet_count']
        listed_count = tweet['public_metrics']['listed_count']

        # Assemble all data in a list
        res = [id, created_at, location, description,username,name,verified, followers_count, following_count, tweet_count,listed_count]
        
        # Append the result to the CSV file
        csvWriter.writerow(res)
        counter += 1

    # When done, close the CSV file
    csvFile.close()

    # Print the number of tweets for this iteration
    print("# of Followers added from this response: ", counter) 


# Run the code in a loop to catch all followers up to limit and push to csv
# Inputs
total_followers = 0
count = 0 # Counting followers per time period
max_count = 350 # Max followers
max_results = 50
flag = True
next_token= None
params = url[1]


# Check if flag is true
while flag:
    # Check if max_count reached
    if count >= max_count:
        break
    print("-------------------")
    print("Token: ",next_token)
    params['next_token']=next_token
    url = create_url(ridge_supply_id, max_results = max_results)        
    json_response = connect_to_endpoint(url[0], url[1],params['next_token'])
    result_count = json_response['meta']['result_count']

    if 'next_token' in json_response['meta']:
        # Save the token to use for next call
        next_token = json_response['meta']['next_token']
        print("Next Token: ",next_token)
        if result_count is not None and result_count > 0 and next_token is not None:
            # print("Start Date: ", start_list[i])
            append_to_csv(json_response, csv_to_file)
            count += result_count
            total_followers += result_count
            print("Total # of followers added: ", total_followers)
            print("count",count)
            print("-------------------")
            time.sleep(5)                
    # If no next token exists
    else:
        if result_count is not None and result_count > 0:
            print("-------------------")
            # print("Start Date: ", start_list[i])
            append_to_csv(json_response, csv_to_file)
            count += result_count
            total_followers += result_count
            print("Total # of followers added: ", total_followers)
            print("count",count)
            print("-------------------")
            time.sleep(5)
        
        #Since this is the final request, turn flag to false to move to the next time period.
        flag = False
        next_token = None
    time.sleep(5)
print("Total number of results: ", total_followers)