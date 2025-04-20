import requests

def fetch_earthquake_data():
    try:
        url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
        response = requests.get(url)
        data = response.json()

        info_list = []

        for quake in data['features']:
            place = quake['properties']['place']
            mag = quake['properties']['mag']
            time = quake['properties']['time']
            print(f"แผ่นดินไหว {mag} ที่ {place}")

        return "\n".join(info_list[:5]) 

    except Exception as e:
        print("❌ fetch error:", e)
        return None