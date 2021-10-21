from database.mongo.connection import client

companies_collection = client.get_collection('companies', name='company')
industries_collection = client.get_collection('companies', name='industry')


