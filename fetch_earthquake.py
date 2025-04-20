import requests

def fetch_earthquake_data():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    data = response.json()

    features = data.get("features", [])
    print("📦 ดึงข้อมูลได้:", len(features), "รายการ")

    if not features:
        return None

    info_list = []
    for quake in features:
        coords = quake['geometry']['coordinates']
        lon, lat = coords[0], coords[1]
        place = quake['properties']['place']
        mag = quake['properties']['mag']

        #เอเชีย
        #latitude:    1° N  ถึง 60° N     (1 ถึง 60)
        #longitude:  25° E ถึง 150° E     (25 ถึง 150)

        #if mag >= 5.0 and 1 <= lat <= 60 and 25 <= lon <= 150:
        if mag >= 1.0: #for test
            info_list.append(f"แผ่นดินไหว {mag} ที่ {place}")

    # ตรวจดูว่ารายการถูกต้อง
    print("📝 รายการที่จัดเตรียมส่ง:", repr(info_list))

    return "\n".join(info_list[:5])
