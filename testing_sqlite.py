#just for learning basics of sqlite db,
#not a part of Basic RESTful API project
import sqlite3

connection = sqlite3.connect("db.data")

cursor = connection.cursor()

create_table = "Create table users (id int , username text, password text)"

cursor.execute(create_table)

user = (1, "usman", "abcdef")

insert_user = "Insert into users values (?,?,?)"

cursor.execute(insert_user,user)

users = [
(2, "ahsan", "12345678"),
(3, "mehrab", "abpqrs")
]
cursor.executemany(insert_user,users)

select_query = "Select * from users"
for row in cursor.execute(select_query):
	print(row)

connection.commit()
connection.close()