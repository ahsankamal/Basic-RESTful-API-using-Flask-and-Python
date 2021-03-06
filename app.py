# pip install Flask, Flask-RESTful, Flask-JWT, Flask-SQLALchemy
import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.items import Item, ItemList
from resources.store import Store,StoreList
# @app.route("/")
# def hello():
#     return "Hello World!"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL","sqlite:///data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turn off flask's SQLALCHEMY modification tracker?
app.secret_key = "abcd"
api = Api(app)
jwt = JWT(app,authenticate, identity) #/auth POST
#Header=>   Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9

#creating routes
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5001/student/rolf
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
   from db import db#importing here to avoid circular imports?
   db.init_app(app)
   app.run(port=5001, debug=True)