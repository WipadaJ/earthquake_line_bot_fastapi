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
        place = quake['properties']['place']
        mag = quake['properties']['mag']

        if mag >= 1.8:
            info_list.append(f"แผ่นดินไหว {mag} ที่ {place}")

    # ตรวจดูว่ารายการถูกต้อง
    print("📝 รายการที่จัดเตรียมส่ง:", repr(info_list))

    return "\n".join(info_list[:5])
