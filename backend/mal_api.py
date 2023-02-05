import os
import requests
from time import sleep
import numpy as np
import pandas as pd
import pickle
from api import API


class MAL_API(API):

    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    headers = {
        'X-MAL-CLIENT-ID': CLIENT_ID,
        'Content-Type': "application/json"
    }

    def get_user_opinion(self, list_status):
        if list_status['status'] in ("completed", "watching", "on_hold", "dropped"):
            return list_status['score']
        
    @classmethod
    def extract_user_entries(cls, user):
        url = f"https://api.myanimelist.net/v2/users/{user}/animelist"
        data = {
            "status": "completed",
            "fields": "list_status",
            "limit": 100
        }
        response = requests.get(url=url, params=data, headers=cls.headers)
        animes = response.json()
        
        if 'error' in animes:
            return None
        else:
            unfiltered_list = [[node['node']['id'], cls.get_user_opinion(node['list_status'])] for node in animes['data']]
            unfiltered_list = list(filter(lambda a, b: b is not None and b != 0, unfiltered_list))

            return np.array(unfiltered_list)

    def get_anime_details(cls, id):
        url = f"https://api.myanimelist.net/v2/anime/{id}"

        data = {
            'fields': "title,mean,recommendations"
        }
        
        response = requests.get(url=url, params=data, headers=cls.headers)
        anime_details = response.json()

        title = anime_details['title']
        rating = anime_details['mean']
        recommendations = np.array([node['node']['id'] for node in anime_details['recommendations']])
        return title, rating, recommendations

    @classmethod
    def pickle_global_entries(cls):
        if not os.path.exists("df.p"):
            n = 20
            anime_ids = []

            for i in range(n):
                print(f"{i}/{n}")
                url = "https://api.myanimelist.net/v2/anime/ranking"

                data = {
                    'ranking_type': "all",
                    'limit': 500,
                    'offset': 500 * i,
                    'fields': "recommendations,score"
                }
                sleep(1)
                response = requests.get(url=url, params=data, headers=cls.headers)

                animes = response.json()
                for node in animes['data']:
                    anime_ids.append(node['node']['id'])

            df = pd.DataFrame(columns=['id', 'name', 'rating', 'recommends'])

            m = 0
            print(f"Total: {len(anime_ids)}")

            for id in anime_ids:
                m += 1
                print(m)
                sleep(0.5)
                title, rating, recommendations = cls.get_anime_details(id)
                details_list = [id, title, rating, recommendations]
                df.loc[len(df)] = details_list

            pickle.dump(df, open("df.p", "wb"))