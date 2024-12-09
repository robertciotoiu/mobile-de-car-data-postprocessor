from mongo_utils import get_mongo_client, get_database, get_collection, create_collection_if_not_exists
from listings_v2_pp import CarListingsProcessor
from post_processors.cubic_capacity_pp import CubicCapacityPostProcessor
from post_processors.mileage_pp import MileagePostProcessor

def main():
    client = get_mongo_client()
    db = get_database(client, 'dev-mobile-de-car-data')
    collection = get_collection(db, 'listings-v2')
    create_collection_if_not_exists(db, 'listings-v2-postprocessed')
    postprocessed_collection = get_collection(db, 'listings-v2-postprocessed')

    car_listings_processor = CarListingsProcessor(collection, postprocessed_collection)
    car_listings_processor.add_post_processor(CubicCapacityPostProcessor())
    car_listings_processor.add_post_processor(MileagePostProcessor())
    car_listings_processor.process_listings()

    print("Post-processing complete")

if __name__ == "__main__":
    main()