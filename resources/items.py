import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
# items=[]
class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price',#all other args in the payload gets erased
		type=float,
		required=True,
		help='this field cant be left blank.'
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
		item = ItemModel(name, data['price'])

		try:
			item.insert()
		except:
			return {"message": "exception occured while inserting item into database."}, 500	
		return item.json(), 201 # to indicate item successful creation, 202 to indicate item will be created soon


	def delete(self,name):
		# global items
		# items = list(filter(lambda x:x['name']!=name, items))
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()
		query = "DELETE from items where name = ?"
		result = cursor.execute(query,(name,))
		connection.commit()
		connection.close()
		return {'message':'Item deleted!'}

	def put(self,name):
		data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name)
		updated_item = ItemModel(name, data['price'])
		if item is None:#create
			updated_item.insert()
		else:#update
			updated_item.update()
		return updated_item.json()	


class ItemList(Resource):
	def get(self):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()
		query = "Select * from items"
		result = cursor.execute(query)
		items = []
		for row in result:
			items.append({"name":row[0],"price":row[1]})
		connection.close()	
		return {"items":items}

