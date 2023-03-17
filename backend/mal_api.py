import os
import requests
from time import sleep
import numpy as np
import pandas as pd
import pickle
from backend.api import API


class MAL_API(API):
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    headers = {
        "X-MAL-CLIENT-ID": CLIENT_ID,
        "Content-Type": "application/json",
    }

    @classmethod
    def get_user_opinion(self, list_status):
        if list_status["status"] in (
            "completed",
            "watching",
            "on_hold",
            "dropped",
        ):
            return list_status["score"]

    @classmethod
    def extract_user_entries(cls, user):
        url = f"https://api.myanimelist.net/v2/users/{user}/animelist"

        end_reached = False
        total_list = []
        i = 0

        while not end_reached:
            data = {
                "status": "completed",
                "fields": "list_status",
                "limit": 100,
                "offset": 100 * i,
            }
            response = requests.get(url=url, params=data, headers=cls.headers)
            animes = response.json()

            if "error" in animes:
                return None
            else:
                unfiltered_list = [
                    [
                        node["node"]["id"],
                        cls.get_user_opinion(node["list_status"]),
                    ]
                    for node in animes["data"]
                ]
                unfiltered_list = list(
                    filter(
                        lambda a: (a[1] is not None and a[1] != 0),
                        unfiltered_list,
                    )
                )
                total_list.extend(unfiltered_list)

            print(f"Got {len(total_list)} ratings...")

            if "next" in animes["paging"]:
                i += 1
            else:
                end_reached = True

        return np.array(total_list)

    @classmethod
    def get_anime_display_details(cls, id_):
        url = f"https://api.myanimelist.net/v2/anime/{id_}"

        data = {"fields": "title,mean"}

        response = requests.get(url=url, params=data, headers=cls.headers)
        anime_details = response.json()

        title = anime_details["title"]
        rating = anime_details["mean"]
        image_url = anime_details["main_picture"]["large"]

        return title, rating, image_url

    @classmethod
    def get_anime_details(cls, id_):
        url = f"https://api.myanimelist.net/v2/anime/{id_}"

        data = {"fields": "title,mean,recommendations"}

        response = requests.get(url=url, params=data, headers=cls.headers)
        anime_details = response.json()

        title = anime_details["title"]
        rating = anime_details["mean"]
        recommendations = np.array(
            [node["node"]["id"] for node in anime_details["recommendations"]]
        )
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
                    "ranking_type": "all",
                    "limit": 500,
                    "offset": 500 * i,
                    "fields": "recommendations,score",
                }
                sleep(1)
                response = requests.get(
                    url=url, params=data, headers=cls.headers
                )

                animes = response.json()
                for node in animes["data"]:
                    anime_ids.append(node["node"]["id"])

            df = pd.DataFrame(columns=["id", "name", "rating", "recommends"])

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


# print(MAL_API.get_anime_display_details(12189))
