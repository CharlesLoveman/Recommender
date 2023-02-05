from flask import Flask, request
from flask_cors import CORS
from backend.mal_api import MAL_API
from backend.engine import recommend


app = Flask(__name__)
CORS(app)
MAL_API.pickle_global_entries()


@app.route("/", methods=['GET'])
def hello_world():
    members = request.args.getlist('members[]')

    #users_info = [MAL_API.extract_user_entries(user) for user in members]
    #recommendation_id = recommend(users_info)
    recommendation_id = 12189
        
    title, rating, image_url = MAL_API.get_anime_display_details(recommendation_id)

    print(members)
    return {"text": f"Hello, {members}!"}

