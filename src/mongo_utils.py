import os
from pymongo import MongoClient

def get_mongo_client():
    client_connection = os.environ['MONGODB_CONNECTION_STRING']
    return MongoClient(client_connection)

def get_database(client, db_name):
    return client[db_name]

def get_collection(db, collection_name):
    return db[collection_name]

def create_collection_if_not_exists(db, collection_name):
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)