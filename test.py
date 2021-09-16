from dotenv import load_dotenv
import os
import pathlib

# cwd = pathlib.Path.cwd()
# print(cwd,'<---this is pathlib')

# name the file we want
env_file_name = 'lrhf97_twit_cred.env'

# designate the path of the file
curr_file = pathlib.Path(__file__).parent

# join them
final_path = curr_file.joinpath(env_file_name)

# load the file
load_dotenv(final_path)

# pull the cred
secret = os.getenv('test_cred')

print(secret)


