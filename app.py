# pip install Flask, Flask-RESTful, Flask-JWT
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.items import Item, ItemList
# @app.route("/")
# def hello():
#     return "Hello World!"

app = Flask(__name__)
app.secret_key = "abcd"
api = Api(app)
jwt = JWT(app,authenticate, identity) #/auth POST
#Header=>   Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
# items = []

#creating routes
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5001/student/rolf
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(port=5001, debug=True)