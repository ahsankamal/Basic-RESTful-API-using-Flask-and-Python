from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):

	def get(self,name):
		store = StoreModel.find_by_name(name)
		if store:
			return store.json()
		return {"message":"Store not found"}, 404 #not found	

	def post(self,name):
		store = StoreModel.find_by_name(name)
		if store:
			return {"message":"store already exist"}, 400 #bad request

		store = StoreModel(name)
		
		try:
			store.save_to_database()
		except:
			return {"message":"error saving to db"}, 500 #internal server error			

		return store.json(), 200
			
	def delete(self,name):
		store = StoreModel.find_by_name(name)
		if store:
			store.delete_from_database()
		return {"message":"store deleted!"}	


	def put(self,name):
		pass	


class StoreList(Resource):

	def get(self):
		return {"stores":[store.json() for store in StoreModel.query.all()]}
