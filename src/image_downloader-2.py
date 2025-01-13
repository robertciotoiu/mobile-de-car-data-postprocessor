import requests

def search_images_on_commons(make, model, year=None):
    # Construct the search query
    base_url = "https://commons.wikimedia.org/w/api.php"
    if year:
        search_query = f"{make} {model} {year} car"
    else:
        search_query = f"{make} {model} car"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": search_query,
        "srnamespace": 6,  # File namespace
        "format": "json"
    }

    # Send the request
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        results = data.get('query', {}).get('search', [])
        if not results and year:  # Retry without year if no results
            print("No results with year; retrying without year...")
            return search_images_on_commons(make, model, year=None)
        image_urls = []
        for result in results:
            title = result['title']
            # Check for valid image file types
            if any(title.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                file_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{title.replace('File:', '')}"
                image_urls.append(file_url)
        return image_urls
    else:
        print("Error fetching data:", response.status_code)
        return []

# Example usage
make = "BMW"
model = "5 Series"
year = "2016"
image_urls = search_images_on_commons(make, model, year)

if image_urls:
    print("Found images:")
    for url in image_urls:
        print(url)
else:
    print("No relevant images found.")
