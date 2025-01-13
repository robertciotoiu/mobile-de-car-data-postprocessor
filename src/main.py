from pymongo import MongoClient
from datetime import datetime
from listings_v2_pp import CarListingsProcessor
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


def get_average_price_per_make_model_year(collection):
    pipeline = [
        # {
        #     "$match": {"sellerType": "FSBO"}
        # },
        {
            "$group": {
                "_id": {"make": "$make", "model": "$model", "year": "$year"},
                "averagePrice": {"$avg": "$grossAmount"}
            }
        }
    ]
    return list(collection.aggregate(pipeline))

def get_closest_to_average_price(collection, make, model, year, average_price):
    pipeline = [
        {
            "$match": {"make": make, "model": model, "year": year}
        },
        {
            "$addFields": {
                "priceDiff": {"$abs": {"$subtract": ["$grossAmount", average_price]}}
            }
        },
        {
            "$sort": {"priceDiff": 1, "scrapeTime": -1}
        },
        {
            "$limit": 1
        },
        {
            "$project": {
                "_id": 0,
                "make": 1,
                "model": 1,
                "year": 1,
                "previewImageSrc": 1,
                "scrapeTime": 1,
                "grossAmount": 1
            }
        }
    ]
    return collection.aggregate(pipeline).next()

def display_latest_images_closest_to_avg_price(db):
    collection = get_collection(db, 'listings-v3-postprocessed')
    average_prices = get_average_price_per_make_model_year(collection)
    
    for avg in average_prices:
        make = avg['_id']['make']
        model = avg['_id']['model']
        year = avg['_id']['year']
        average_price = avg['averagePrice']
        closest_doc = get_closest_to_average_price(collection, make, model, year, average_price)
        
        # if 'grossAmount' in closest_doc:
        # print(f"Make: {closest_doc['make']}, Model: {closest_doc['model']}, Year: {closest_doc['year']}, Preview Image Src: {closest_doc['previewImageSrc']}, Scrape Time: {closest_doc['scrapeTime']}, Gross Amount: {closest_doc['grossAmount']}, Average Price: {average_price}")
        # print("--------------------------------------------------------------------------------------------------------------------")

    # print average prices
    # print("Average Prices:")
    # for avg in average_prices:
    #     print(f"Make: {avg['_id']['make']}, Model: {avg['_id']['model']}, Year: {avg['_id']['year']}, Average Price: {avg['averagePrice']}")

    # print the number of cl
    print(f"Number of average prices: {len(average_prices)}")
    
    print("Post-processing and image retrieval complete")

def get_highest_price_per_make_model_year(collection):
    pipeline = [
        {
            "$match": {"sellerType": "FSBO"}
        },
        {
            "$group": {
                "_id": {"make": "$make", "model": "$model", "year": "$year"},
                "highestPrice": {"$max": "$grossAmount"}
            }
        }
    ]
    return list(collection.aggregate(pipeline))

def get_closest_to_highest_price(collection, make, model, year, highest_price):
    pipeline = [
        {
            "$match": {"make": make, "model": model, "year": year, "sellerType": "FSBO"}
        },
        {
            "$addFields": {
                "priceDiff": {"$abs": {"$subtract": ["$grossAmount", highest_price]}}
            }
        },
        {
            "$sort": {"priceDiff": 1, "scrapeTime": -1}
        },
        {
            "$limit": 1
        },
        {
            "$project": {
                "_id": 0,
                "make": 1,
                "model": 1,
                "year": 1,
                "previewImageSrc": 1,
                "scrapeTime": 1,
                "grossAmount": 1
            }
        }
    ]
    return collection.aggregate(pipeline).next()

def display_latest_images_closest_to_highest_price(db):
    collection = get_collection(db, 'listings-v3-postprocessed')
    highest_prices = get_highest_price_per_make_model_year(collection)
    
    for price in highest_prices:
        make = price['_id']['make']
        model = price['_id']['model']
        year = price['_id']['year']
        highest_price = price['highestPrice']
        closest_doc = get_closest_to_highest_price(collection, make, model, year, highest_price)
        
        if 'grossAmount' in closest_doc:
            print(f"Make: {closest_doc['make']}, Model: {closest_doc['model']}, Year: {closest_doc['year']}, Preview Image Src: {closest_doc['previewImageSrc']}, Scrape Time: {closest_doc['scrapeTime']}, Gross Amount: {closest_doc['grossAmount']}, Highest Price: {highest_price}")
        print("--------------------------------------------------------------------------------------------------------------------")

    print("Highest Prices:")
    for price in highest_prices:
        print(f"Make: {price['_id']['make']}, Model: {price['_id']['model']}, Year: {price['_id']['year']}, Highest Price: {price['highestPrice']}")

    print("Post-processing and image retrieval complete")

def main():
    client = get_mongo_client()
    db = get_database(client, 'dev-mobile-de-car-data')
    collection = get_collection(db, 'listings-v3-postprocessed')
    create_indexes(collection)
    # process_car_listings(db)
    display_latest_images_closest_to_highest_price(db)

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