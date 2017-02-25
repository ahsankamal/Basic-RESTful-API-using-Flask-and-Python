import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()
create_user_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
cursor.execute(create_user_table)

create_items_table = "Create table if not exists items (name text, price real)"
cursor.execute(create_items_table)

connection.commit()
connection.close()