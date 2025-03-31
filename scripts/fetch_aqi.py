# import os
# import requests
# import psycopg2
# from datetime import datetime
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry

# # 📌 ตั้งค่า API Key และฐานข้อมูลจาก Environment Variables
# API_KEY = os.getenv("AIRVISUAL_API_KEY", "YOUR_API_KEY")
# DB_CONNECTION = {
#     "dbname": os.getenv("DB_NAME", "aqi_project"),
#     "user": os.getenv("DB_USER", "postgres"),
#     "password": os.getenv("DB_PASSWORD", "postgres"),
#     "host": os.getenv("DB_HOST", "localhost"),
#     "port": os.getenv("DB_PORT", "5432")
# }

# # 📌 รายชื่อเมืองที่ต้องดึงข้อมูล
# CITIES = [
#     {"city": "Bangkok", "state": "Bangkok", "country": "Thailand"},
#     {"city": "Nakhon Pathom", "state": "Nakhon Pathom", "country": "Thailand"},
#     {"city": "Pathum Thani", "state": "Pathum Thani", "country": "Thailand"}
# ]

# # 🔄 ตั้งค่าการ retry request
# session = requests.Session()
# retries = Retry(total=3, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
# session.mount("https://", HTTPAdapter(max_retries=retries))

# def fetch_aqi():
#     """ ดึงข้อมูล AQI จาก API และบันทึกลงฐานข้อมูล """
#     try:
#         with psycopg2.connect(**DB_CONNECTION) as conn:
#             with conn.cursor() as cur:
#                 for city_info in CITIES:
#                     city, state, country = city_info["city"], city_info["state"], city_info["country"]
#                     api_url = f"https://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={API_KEY}"
                    
#                     print(f"📡 กำลังดึงข้อมูล AQI สำหรับ {city} ...")
#                     response = session.get(api_url)
#                     data = response.json()

#                     if response.status_code == 200 and "data" in data:
#                         aqi_value = data["data"]["current"]["pollution"]["aqius"]
#                         timestamp = datetime.now()

#                         cur.execute(
#                             "INSERT INTO aqi_data (city, aqi_value, timestamp) VALUES (%s, %s, %s)",
#                             (city, aqi_value, timestamp)
#                         )
#                         conn.commit()
#                         print(f"✅ ดึงข้อมูลสำเร็จ: {city} AQI {aqi_value} บันทึกเมื่อ {timestamp}")
#                     else:
#                         print(f"⚠️ ไม่พบข้อมูลสำหรับ {city}: {data.get('data', {}).get('message', 'Unknown error')}")
#     except Exception as e:
#         print(f"❌ เกิดข้อผิดพลาด: {e}")

# if __name__ == "__main__":
#     fetch_aqi()
