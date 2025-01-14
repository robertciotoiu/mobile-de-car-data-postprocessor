import pymongo

def get_database(db_name):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client[db_name]

def get_collection(db, collection_name):
    return db[collection_name]

def extract_unique_bmw_model_year(collection, output_file):
    pipeline = [
        {
            "$match": {
                "make": "BMW"
            }
        },
        {
            "$group": {
                "_id": {"model": "$model", "year": "$year"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "model": "$_id.model",
                "year": "$_id.year"
            }
        },
        {
            "$sort": {
                "model": 1,
                "year": 1
            }
        }
    ]
    results = collection.aggregate(pipeline)
    
    with open(output_file, 'w') as file:
        for result in results:
            line = f"BMW {result['model']} {result['year']}\n"
            file.write(line)

if __name__ == '__main__':
    db = get_database('dev-mobile-de-car-data')
    collection = get_collection(db, 'listings-v3-postprocessed')
    extract_unique_bmw_model_year(collection, 'src/bmw-image-pp/unique_bmw_model_year.txt')