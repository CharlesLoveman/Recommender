from flask import Flask, request
from flask_cors import CORS
from backend.mal_api import MAL_API
from backend.engine import recommend


app = Flask(__name__)
CORS(app)
MAL_API.pickle_global_entries()


@app.route("/", methods=["GET"])
def hello_world():
    members = request.args.getlist("members[]")
    users_info = []
    for user in members:
        print(f"Getting ratings for user {user}...")
        user_info = MAL_API.extract_user_entries(user)
        if user_info is None:
            return {"Error": "User profile is private."}
        if not len(user_info):
            return {"Error": "User has no ratings."}
        users_info.append(user_info)

    if len(users_info):
        results = []
        print("Generating recommendations...")
        recommendations = recommend(users_info)
        for id_ in recommendations:
            title, rating, image_url = MAL_API.get_anime_display_details(id_)
            id_ = str(id_)
            results.append({
                "id": id_,
                "title": title,
                "rating": rating,
                "image_url": image_url,
            })

        print("Done!")

        return results

    return {"Error": "User not found."}