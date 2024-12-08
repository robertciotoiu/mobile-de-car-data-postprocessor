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

def convert_cubic_capacity_to_float(car):
    cubic_capacity = car.get('cubicCapacity', '')
    if cubic_capacity:
        numeric_capacity = ''.join(filter(str.isdigit, cubic_capacity.replace(",", "")))
        if numeric_capacity:
            cubic_capacity_float = float(numeric_capacity) if numeric_capacity else None
            return cubic_capacity_float
    return None

def process_car_listings(collection, postprocessed_collection, batch_size=1000):
    processed_cars = []
    for car in collection.find():
        cubic_capacity_float = convert_cubic_capacity_to_float(car)
        processed_car = car.copy()
        processed_car['cubicCapacity'] = cubic_capacity_float
        processed_cars.append(processed_car)
        if len(processed_cars) == batch_size:
            postprocessed_collection.insert_many(processed_cars)
            processed_cars = []
        
    if processed_cars:
        postprocessed_collection.insert_many(processed_cars)


def main():
    client = get_mongo_client()
    db = get_database(client, 'dev-mobile-de-car-data')
    collection = get_collection(db, 'listings-v2')
    create_collection_if_not_exists(db, 'listings-v2-postprocessed')
    postprocessed_collection = get_collection(db, 'listings-v2-postprocessed')
    process_car_listings(collection, postprocessed_collection)
    print("Post-processing complete")

if __name__ == "__main__":
    main()
