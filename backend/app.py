from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.get("/")
def hello_world():
    print("hello")
    return {"text": "Hello, World!"}
