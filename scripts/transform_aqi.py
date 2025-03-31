# import os
# import psycopg2

# # 📌 ตั้งค่าการเชื่อมต่อฐานข้อมูลจาก Environment Variables
# DB_CONNECTION = {
#     "dbname": os.getenv("DB_NAME", "aqi_project"),
#     "user": os.getenv("DB_USER", "postgres"),
#     "password": os.getenv("DB_PASSWORD", "postgres"),
#     "host": os.getenv("DB_HOST", "localhost"),
#     "port": os.getenv("DB_PORT", "5432")
# }

# def transform_aqi():
#     """ แปลงข้อมูล AQI เป็นค่าเฉลี่ยรายวัน และทำความสะอาดข้อมูล """
#     try:
#         with psycopg2.connect(**DB_CONNECTION) as conn:
#             with conn.cursor() as cur:
#                 print("🔄 เริ่มกระบวนการแปลงข้อมูล AQI...")

#                 # ลบข้อมูลที่ AQI เป็น NULL
#                 cur.execute("DELETE FROM aqi_data WHERE aqi_value IS NULL;")

#                 # สร้างตารางถ้ายังไม่มี
#                 cur.execute("""
#                     CREATE TABLE IF NOT EXISTS aqi_daily_avg (
#                         city TEXT NOT NULL,
#                         date DATE NOT NULL,
#                         avg_aqi FLOAT,
#                         PRIMARY KEY (city, date)
#                     );
#                 """)

#                 # ลบข้อมูลซ้ำกัน
#                 cur.execute("TRUNCATE TABLE aqi_daily_avg;")

#                 # คำนวณค่าเฉลี่ยรายวันและบันทึกลงตาราง aqi_daily_avg
#                 cur.execute("""
#                     INSERT INTO aqi_daily_avg (city, date, avg_aqi)
#                     SELECT city, DATE(timestamp) as date, AVG(aqi_value) as avg_aqi
#                     FROM aqi_data
#                     GROUP BY city, date
#                     ON CONFLICT (city, date) 
#                     DO UPDATE SET avg_aqi = EXCLUDED.avg_aqi;
#                 """)

#                 conn.commit()
#                 print("✅ การแปลงข้อมูล AQI เสร็จสมบูรณ์")
#     except Exception as e:
#         print(f"❌ เกิดข้อผิดพลาดในการแปลงข้อมูล: {e}")

# if __name__ == "__main__":
#     transform_aqi()
