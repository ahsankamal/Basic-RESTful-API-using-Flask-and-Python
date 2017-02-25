from models.user import UserModel
# from werkzeug.security import safe_str_cmp, safe_str_cmp(user.password == password:)

#in memory
# users = [
# 	User(1,"ahsan","ehsan60kamal")
# ]

# username_mapping = {u.username:u for u in users}
# userid_mapping = {u.id:u for u in users}

def authenticate(username, password):
	# user = username_mapping.get(username,None)
	user = UserModel.find_by_username(username)
	if user and user.password == password:
		return user


def identity(payload):
	user_id = payload['identity']
	# return userid_mapping.get(user_id,None)
	return UserModel.find_by_id(user_id)

