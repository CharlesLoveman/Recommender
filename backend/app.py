from flask import Flask, request
from flask_cors import CORS
from mal_api import MAL_API


app = Flask(__name__)
CORS(app)
MAL_API.pickle_global_entries()

@app.route("/", methods=['GET'])
def hello_world():
    members = request.args.getlist('members[]')
    
    for user in members:
        user_entries = MAL_API.extract_user_entries(user)
        

    print(members)
    return {"text": f"Hello, {members}!"}

