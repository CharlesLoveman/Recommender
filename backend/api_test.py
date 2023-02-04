import os
import requests
import secrets
import json
from time import sleep
from pprint import pprint
import numpy as np
import pandas as pd
import pickle

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


# 1. Generate a new Code Verifier / Code Challenge.
def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]


# 2. Print the URL needed to authorise your application.
def get_authorisation_code(code_challenge: str):

    url = """https://myanimelist.net/v1/oauth2/authorize"""
    data = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code_challenge': code_challenge,
    }
    response = requests.get(url, data)
    auth_code = response.json()
    print(auth_code)
    return 


# 3. Once you've authorised your application, you will be redirected to the webpage you've
#    specified in the API panel. The URL will contain a parameter named "code" (the Authorisation
#    Code). You need to feed that code to the application.
def generate_new_token(authorisation_code: str, code_verifier: str) -> dict:
    global CLIENT_ID, CLIENT_SECRET

    url = 'https://myanimelist.net/v1/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': authorisation_code,
        'code_verifier': code_verifier,
        'grant_type': 'authorization_code'
    }

    response = requests.post(url, data)
    response.raise_for_status()  # Check whether the request contains errors

    token = response.json()
    response.close()
    print('Token generated successfully!')

    with open('token.json', 'w') as file:
        json.dump(token, file, indent=4)
        print('Token saved in "token.json"')

    return token


# 4. Test the API by requesting your profile information
def print_user_info(access_token: str):
    url = 'https://api.myanimelist.net/v2/users/@me'
    response = requests.get(url, headers={
        'Authorization': f'Bearer {access_token}'
        })
    response.raise_for_status()
    user = response.json()
    response.close()

    print(f"\n>>> Greetings {user['name']}! <<<")


#code_verifier = code_challenge = get_new_code_verifier()
#authorisation_code = get_authorisation_code(code_challenge)
# print(authorisation_code)
# token = generate_new_token(authorisation_code, code_verifier)

# print_user_info(token['access_token'])

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

n = 20
anime_ids = []


for i in range(n):
    print(f"{i}/{n}")
    url = "https://api.myanimelist.net/v2/anime/ranking"
    headers = {
        'X-MAL-CLIENT-ID': CLIENT_ID,
        'Content-Type': "application/json"
    }

    data = {
        'ranking_type': "all",
        'limit': 500,
        'offset': 500 * i,
        'fields': "recommendations,score"
    }
    sleep(1)
    response = requests.get(url=url, params=data, headers=headers)

    animes = response.json()

    #pprint(animes)

    

    for node in animes['data']:
        anime_ids.append(node['node']['id'])


df = pd.DataFrame(columns=['id', 'name', 'rating', 'recommends'])

m = 0
print(f"Total: {len(anime_ids)}")

for id in anime_ids:
    m += 1
    print(m)
    url = f"https://api.myanimelist.net/v2/anime/{id}"
    headers = {
        'X-MAL-CLIENT-ID': CLIENT_ID,
        'Content-Type': "application/json"
    }

    data = {
        'fields': "title,mean,recommendations"
    }
    sleep(0.5)
    response = requests.get(url=url, params=data, headers=headers)
    anime_details = response.json()

    #pprint(anime_details)

    title = anime_details['title']
    rating = anime_details['mean']
    recommendations = np.array([node['node']['id'] for node in anime_details['recommendations']])

    details_list = [id, title, rating, recommendations]
    df.loc[len(df)] = details_list


pickle.dump(df, open("df.p", "wb"))
   