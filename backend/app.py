from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
def hello_world():
    members = request.args.getlist('members[]')
    print(members)
    return {"text": f"Hello, {members}!"}