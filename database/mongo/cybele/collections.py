import motor.motor_asyncio
from decouple import config

MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.core

locations = database.get_collection('locations')
images = database.get_collection('images')
pieces = database.get_collection('pieces')
