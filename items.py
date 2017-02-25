import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

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
		# item = next(filter(lambda x:x['name']==name, items), None) #returns first matched item, otherwise None
		# return {"item": item}, 200 if item else 404
		item = Item.find_by_name(name)
		if item:
			return item
		return {"message":"Item not found"},404

	@classmethod	
	def find_by_name(cls,name):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()
		query = "SELECT * from items where name = ?"
		result = cursor.execute(query,(name,))
		row = result.fetchone()
		connection.close()
		if row:
			return {"item":{"name":row[0],"price":row[1]}}

	def post(self,name):
		# if next(filter(lambda x:x['name']==name, items), None): #returns first matched item, otherwise None
		# 	return {"Item {} already exist.".format(name)}, 400 #bad request
		item = self.find_by_name(name)
		if item:
			return {"message":"Item {} already exist.".format(name)}, 400
		data = Item.parser.parse_args()
		item = { "name":name, "price": data['price'] }
		# items.append(item)
		try:
			self.insert(item)
		except:
			return {"message": "exception occured while inserting item into database."}, 500	
		return item, 201 # to indicate item successful creation, 202 to indicate item will be created soon

	@classmethod
	def insert(cls,item):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()
		query = "Insert into items values (?,?)"
		cursor.execute(query,(item['name'],item['price']))
		connection.commit()
		connection.close()

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

	def put(self,name):#idempotent
		# data = request.get_json()
		# data = parser.parse_args()
		data = Item.parser.parse_args()
		# item = next(filter(lambda x:x['name']==name, items), None) 
		item = self.find_by_name(name)
		updated_item = {"name":name,"price":data['price']}
		if item is None:#create
			# item = {"name":name,"price":data['price']}
			# items.append(item)
			self.insert(updated_item)
		else:#update
			self.update(updated_item)
		return updated_item	
	@classmethod	
	def update(cls,item):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()
		query = "Update items set price = ? where name = ?"
		cursor.execute(query,(item['price'],item['name']))
		connection.commit()
		connection.close()	
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

