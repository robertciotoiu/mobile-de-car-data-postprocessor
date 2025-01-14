import os
import pymongo

def get_database(db_name):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client[db_name]

def get_collection(db, collection_name):
    return db[collection_name]

def extract_unique_make_model_year(collection):
    pipeline = [
        {
            "$group": {
                "_id": {"make": "$make", "model": "$model", "year": "$year"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "make": "$_id.make",
                "model": "$_id.model",
                "year": "$_id.year"
            }
        },
        {
            "$sort": {
                "make": 1,
                "model": 1,
                "year": 1
            }
        }
    ]
    results = collection.aggregate(pipeline)
    return list(results)

def postprocess(results):
    # Delete all entries with year 'None', 'Other' or model 'None', 'Other' (case insensitive)
    results = [result for result in results if str(result['year']).lower() not in ['none', 'other'] and result['model'].lower() not in ['none', 'other']]
    return results

def save_to_file(output_file, results):
    if os.path.exists(output_file):
        os.remove(output_file)
        
    with open(output_file, 'w') as file:
        for result in results:
            line = f"{result['make']} : {result['model']} : {result['year']}\n"
            file.write(line)

    
if __name__ == '__main__':
    db = get_database('dev-mobile-de-car-data')
    collection = get_collection(db, 'listings-v3-postprocessed')
    results = extract_unique_make_model_year(collection)
    postprocessed_results = postprocess(results)
    save_to_file('src/image-downloader/unique_make_model_year.txt', postprocessed_results)