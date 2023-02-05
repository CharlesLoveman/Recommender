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

    #users_info = [MAL_API.extract_user_entries(user) for user in members]
    #recommendation_id = recommend(users_info)
    recommendations = [12189, 49387, 50330, 50197, 41514]

    results = []
    for id in recommendations:
        title, rating, image_url = MAL_API.get_anime_display_details(id)
        results.append({
            "id": id,
            "title": title,
            "rating": rating,
            "image_url": image_url,
        })
    return results