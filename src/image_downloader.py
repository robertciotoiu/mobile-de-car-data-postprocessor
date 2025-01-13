import requests
import os
from pymongo import MongoClient
from urllib.parse import urlparse

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
db = client['nextca']  # Database name
collection = db['car_images']  # Collection name

# Directory to store images
public_folder = os.path.join(os.getcwd(), 'car-images')
os.makedirs(public_folder, exist_ok=True)

# Function to search Wikimedia Commons for images
def search_wikimedia_commons(car_make, car_model, car_year):
    search_query = f"{car_make} {car_model} {car_year}"
    url = f"https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search&srsearch={search_query}&utf8=&srlimit=1"
    response = requests.get(url)
    data = response.json()
    
    if 'query' in data and 'search' in data['query']:
        search_results = data['query']['search']
        if search_results:
            page_id = search_results[0]['pageid']
            image_info_url = f"https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=images&pageids={page_id}"
            image_info_response = requests.get(image_info_url)
            image_info_data = image_info_response.json()
            
            if 'query' in image_info_data and 'pages' in image_info_data['query']:
                page_data = image_info_data['query']['pages'][str(page_id)]
                images = page_data.get('images', [])
                for img in images:
                    if 'title' in img:
                        image_filename = img['title']
                        image_url = f"https://upload.wikimedia.org/wikipedia/commons/{image_filename}"
                        return image_url
    return None

# Function to download the image
def download_image(url, file_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check if request is successful
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded image: {file_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return False

# Function to save attribution data to MongoDB
def save_attribution_to_db(image_url, file_path, attribution):
    image_data = {
        "image_url": image_url,
        "file_path": file_path,
        "attribution": attribution
    }
    collection.insert_one(image_data)
    print(f"Saved attribution data for {file_path} in MongoDB.")

def get_wikimedia_metadata(image_url):
    api_url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "imageinfo",
        "iiprop": "extmetadata",
        "format": "json",
        "titles": os.path.basename(image_url)
    }
    response = requests.get(api_url, params=params)
    data = response.json()
    pages = data.get("query", {}).get("pages", {})
    for page_id, page_data in pages.items():
        if "imageinfo" in page_data:
            extmetadata = page_data["imageinfo"][0]["extmetadata"]
            author = extmetadata.get("Artist", {}).get("value", "Unknown author")
            license = extmetadata.get("LicenseShortName", {}).get("value", "Unknown license")
            return author, license
    return "Unknown author", "Unknown license"


# Main function to process images based on make, model, and year
def process_car_images(car_make, car_model, car_year):
    image_url = search_wikimedia_commons(car_make, car_model, car_year)
    print(f"Image URL: {image_url}")
    if image_url:
        parsed_url = urlparse(image_url)
        filename = os.path.basename(parsed_url.path)
        file_path = os.path.join(public_folder, filename)
        
        if download_image(image_url, file_path):
            author, license = get_wikimedia_metadata(image_url)
            attribution = {
                "author": "Wikimedia Commons contributor",
                "source": image_url,
                "license": "CC BY-SA 4.0"
            }
            save_attribution_to_db(image_url, file_path, attribution)

if __name__ == '__main__':
    # Example: Process a BMW 3 series 2020
    process_car_images('Porsche', '911', '1981')

# https://en.wikipedia.org/w/api.php?action=query&list=allimages&aiprop=url&format=json&ailimit=2&ai=porsche%20911&aiprop=usermetadata