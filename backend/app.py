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
        user_info = MAL_API.extract_user_entries(user)
        if user_info is None:
            return {"error": "User profile is private."}
        if not len(user_info):
            return {"error": "User has no ratings."}
        users_info.append(user_info)

    if len(users_info):
        results = []
        recommendations = recommend(users_info)
        for id in recommendations:
            title, rating, image_url = MAL_API.get_anime_display_details(id)
            id = str(id)
            results.append({
                "id": id,
                "title": title,
                "rating": rating,
                "image_url": image_url,
            })
        return results

    return {"error": "User not found."}