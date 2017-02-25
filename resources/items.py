from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type=float,
		required=True,
		help='this field cant be left blank.'
		)
	parser.add_argument('store_id',
		type=int,
		required=True,
		help='every item needs a store'
		)
	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {"message":"Item not found"},404


	def post(self,name):
		# if next(filter(lambda x:x['name']==name, items), None): #returns first matched item, otherwise None
		# 	return {"Item {} already exist.".format(name)}, 400 #bad request
		item = ItemModel.find_by_name(name)
		if item:
			return {"message":"Item {} already exist.".format(name)}, 400
		data = Item.parser.parse_args()
		item = ItemModel(name, data['price'], data['store_id'])

		try:
			item.save_to_database()
		except:
			return {"message": "exception occured while inserting item into database."}, 500	
		return item.json(), 201 # to indicate item successful creation, 202 to indicate item will be created soon


	def delete(self,name):
		# global items
		# items = list(filter(lambda x:x['name']!=name, items))
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_database()
			return {'message':'Item deleted!'}

	def put(self,name):
		data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name)
		if item is None:#create
			item = ItemModel(name, data['price'], data['store_id'])
		else:#update
			item.price = data['price']
			item.store_id = data['store_id']

		item.save_to_database()	
		return item.json()	


class ItemList(Resource):
	def get(self):	
		return {"items":[item.json() for item in ItemModel.query.all()]}

