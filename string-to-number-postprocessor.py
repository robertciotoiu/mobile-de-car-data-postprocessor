import os
from pymongo import MongoClient

# Connect to MongoDB
# read the connection string from the environment variable
clientConnection = os.environ['MONGODB_CONNECTION_STRING']

client = MongoClient(clientConnection)
db = client['dev-mobile-de-car-data']
collection = db['listings-v2']

# Iterate through each car listing and transform the cubicCapacity field
for car in collection.find():
    cubic_capacity = car.get('cubicCapacity', '')
    if cubic_capacity:
        # Remove non-numeric characters (like commas, cc, etc.)
        numeric_capacity = ''.join(filter(str.isdigit, cubic_capacity.replace(",", "")))
        print(f"Car: {car['_id']}, cubicCapacity: {cubic_capacity}, numericCapacity: {numeric_capacity}")

        if numeric_capacity:
            # Update the document with the numeric value
            # collection.update_one({'_id': car['_id']}, {'$set': {'cubicCapacity': int(numeric_capacity)}})
            # Instead of updating the document, insert the car into a new collection with the numeric value. The new collection will be named 'listings-v2-postprocessed'

            # Create a new car listing with the numeric value
            processed_car = car.copy()
            processed_car['cubicCapacity'] = int(numeric_capacity) if numeric_capacity else None

            # Check if the collection "listings-v2-postprocessed" exists. If not, create it
            if 'listings-v2-postprocessed' not in db.list_collection_names():
                db.create_collection('listings-v2-postprocessed')
            postprocessed_collection = db['listings-v2-postprocessed']

            # Insert the processed car into the new collection
            postprocessed_collection.insert_one(processed_car)

            # Break the for loop after processing the first car for demonstration purposes
            break

            

