import requests
import os
from pymongo import MongoClient

headers = {
    "User-Agent": "NextCa/1.0 (robert.ciotoiu@gmail.com)"
}

def download_image(query):
    base_url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "uselang": "en",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap|drawing -fileres:0 {query}",
        "gsrlimit": 1,
        "gsroffset": 0,
        "gsrinfo": "totalhits|suggestion",
        "gsrprop": "size|wordcount|timestamp|snippet",
        "prop": "info|imageinfo|entityterms",
        "inprop": "url",
        "gsrnamespace": 6,
        "iiprop": "url|size|mime|extmetadata",
        "iiurlheight": 180,
        "wbetterms": "label"
    }

    response = requests.get(base_url, params=params, headers=headers)
    data = response.json()

    pages = data.get("query", {}).get("pages", {})
    if not pages:
        fallback_method(query)
        return False

    first_page = next(iter(pages.values()))
    image_info = first_page.get("imageinfo", [])
    if not image_info:
        fallback_method(query)
        return False

    image_url = image_info[0].get("url")
    if not image_url:
        fallback_method(query)
        return False

    extmetadata = image_info[0].get("extmetadata", {})
    artist = extmetadata.get("Artist", {}).get("value", "Unknown artist")
    file_name = extmetadata.get("ObjectName", {}).get("value", "Unknown file name")
    file_href = first_page.get("fullurl", "No file URL available")
    license_url = extmetadata.get("LicenseUrl", {}).get("value", "No license URL available")
    license_name = extmetadata.get("LicenseShortName", {}).get("value", "No license name available")

    attribution = f'{artist}, <a href="{file_href}">{file_name}</a>, <a href="{license_url}" rel="license">{license_name}</a>'
    
    print(f"Attribution: {attribution}")
    download_and_save_image(image_url, query, attribution)
    return True

def download_and_save_image(image_url, query, attribution):
    file_name = f"{query.replace(' ', '_')}.jpg"
    file_name_full_path = os.path.join(download_path, file_name)

    if os.path.exists(file_name_full_path):
        print(f"Image already downloaded as {file_name_full_path}")
        return
    
    response = requests.get(image_url, headers=headers)
    if response.status_code == 200:
        with open(file_name_full_path, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded and saved as {file_name_full_path}")

        # Save attribution to MongoDB
        collection.insert_one({
            "_id": file_name,
            "attribution": attribution
        })
        print(f"Attribution saved to MongoDB with ID: {file_name}")
    else:
        print("Failed to download image")

def fallback_method(query):
    print(f"No image found for query: {query}")
    # Implement fallback logic here

client = MongoClient('mongodb://localhost:27017/')
db = client['nextca']
collection = db['car_image_attribution']

download_path = "src/image-downloader/images/"
if not os.path.exists(download_path):
    os.makedirs(download_path)

if __name__ == "__main__":
    query = "Wiesmann MF 4 2006"
    
    # Read the list of unique make, model, year combinations from unique_make_model_year.txt into a list without BMW make
    with open('src/image-downloader/unique_make_model_year.txt', 'r') as file:
        unique_make_model_year = [line.strip() for line in file.readlines() if not line.startswith('BMW')]
    
    # Add to the list a list with BMW make from read from bmw-model-code-map.json
    import json
    with open('src/image-downloader/bmw-model-code-map.json', 'r') as file:
        bmw_models = json.load(file)
    
    bmw_make = 'BMW'
    bmw_make_models = [f"{bmw_make} : {model.split('/')[0]}" for model in bmw_models.values()]
    unique_make_model_year.extend(bmw_make_models)
    
    # Remove only the first : from each element in unique_make_model_year
    unique_make_model_year = [line.replace(' : ', ' ', 1) for line in unique_make_model_year]
    
    # Download images for each element in unique_make_model_year
    for query in unique_make_model_year:
        # First query with the year, we need to remove : from the query
        firstQuery = query.replace(' : ', ' ').strip()
        if not download_image(firstQuery):
            # retry without the year. We take the text until ':' character
            secondQuery = query.split(':')[0].strip()
            download_image(secondQuery)