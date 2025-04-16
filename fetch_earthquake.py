import requests

def fetch_earthquake_data():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
    response = requests.get(url)
    data = response.json()

    for quake in data['features']:
        place = quake['properties']['place']
        mag = quake['properties']['mag']
        time = quake['properties']['time']
        print(f"แผ่นดินไหว {mag} ที่ {place}")