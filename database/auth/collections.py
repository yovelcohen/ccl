from database.connection import create_mongo_client, client

user_collection = client.get_collection('users')
admin_collection = client.get_collection('admins')
