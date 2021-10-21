from database.mongo.connection import client

user_collection = client.get_collection('users')
admin_collection = client.get_collection('admins')
