from pymongo import MongoClient
from datetime import datetime
from listings_pp import CarListingsProcessor
from mongo_utils import create_collection_if_not_exists
from post_processors.cubic_capacity_pp import CubicCapacityPostProcessor
from post_processors.door_count_pp import DoorCountPostProcessor
from post_processors.mileage_pp import MileagePostProcessor
from post_processors.power_pp import PowerPostProcessor
from post_processors.year_extractor_pp import YearExtractorPostProcessor

def get_mongo_client():
    # Replace with your MongoDB connection details
    return MongoClient('mongodb://localhost:27017/')

def get_database(client, db_name):
    return client[db_name]

def get_collection(db, collection_name):
    return db[collection_name]

def main():
    client = get_mongo_client()
    db = get_database(client, 'dev-mobile-de-car-data')
    collection = get_collection(db, 'listings-v3-postprocessed')
    create_indexes(collection)
    process_car_listings(db)

def create_indexes(collection):
    collection.create_index([("make", 1), ("model", 1), ("year", 1), ("sellerType", 1)])

def process_car_listings(db):
    collection = get_collection(db, 'listings_v3')

    create_collection_if_not_exists(db, 'listings-v3-postprocessed')
    postprocessed_collection = get_collection(db, 'listings-v3-postprocessed')

    car_listings_processor = CarListingsProcessor(collection.find(), postprocessed_collection)
    car_listings_processor.add_post_processor(CubicCapacityPostProcessor())
    car_listings_processor.add_post_processor(MileagePostProcessor())
    car_listings_processor.add_post_processor(PowerPostProcessor())
    car_listings_processor.add_post_processor(DoorCountPostProcessor())
    car_listings_processor.add_post_processor(YearExtractorPostProcessor())
    car_listings_processor.process_listings()

if __name__ == "__main__":
    main()