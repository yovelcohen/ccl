import os
from urllib.parse import quote_plus

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient


class MongoConnection:
    def __init__(self, db, as_async):
        self.db = db
        self.as_async = as_async
        self._password = None

    @property
    def password(self):
        password = os.environ['MONGO']
        self._password = quote_plus(password)
        return self._password

    def _get_db(self):
        """
        connects to the cluster and retrieves a cn a/sync client as specified in class initialization
        """
        if os.environ.get('LOCAL', False):
            url = f"mongodb://mongodb0.example.com:27017"
        else:
            username = quote_plus(os.environ['MONGO'])
            url = ''

        db = MongoClient(url)[self.db] if self.as_async is False else AsyncIOMotorClient(url)[self.db]
        return db

    def connect_to_db(self):
        return self._get_db()


def create_mongo_client(db, as_async):
    """
    returns a Mongo DB
    """
    connection = MongoConnection(db, as_async)
    return connection.connect_to_db()


client = create_mongo_client('users', as_async=True)

user_collection = client.get_collection('users')
admin_collection = client.get_collection('admins')
