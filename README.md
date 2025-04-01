# ระบบดึงข้อมูลคุณภาพอากาศ (Air Quality Data Pipeline)

## ภาพรวม
โครงการนี้เป็นระบบดึงและประมวลผลข้อมูลดัชนีคุณภาพอากาศ (AQI) สำหรับกรุงเทพฯ นนทบุรี และปทุมธานี โดยใช้ **Apache Airflow** และ **PostgreSQL** ระบบนี้ช่วยให้สามารถเก็บรวบรวม ทำความสะอาด และจัดเก็บข้อมูลเพื่อการวิเคราะห์ต่อไปได้อย่างอัตโนมัติ

## วัตถุประสงค์ของโครงการ
1. ดึงข้อมูล AQI รายวันจาก AirVisual API
2. แปลงข้อมูลให้อยู่ในรูปแบบที่เหมาะสมกับการใช้งาน
3. ตรวจสอบคุณภาพของข้อมูล (Data Quality Check)
4. จัดเก็บข้อมูลใน PostgreSQL
5. ใช้ SQL เพื่อวิเคราะห์ข้อมูลและตอบคำถามทางธุรกิจ
6. สร้าง Dashboard เพื่อนำเสนอข้อมูล AQI

## คุณสมบัติของโครงการ
- **ดึงข้อมูล**: รับข้อมูล AQI จาก API ภายนอก
- **แปลงข้อมูล**: ทำความสะอาดและจัดรูปแบบข้อมูลให้เหมาะสมกับการใช้งาน
- **จัดเก็บข้อมูล**: บันทึกข้อมูลลงในฐานข้อมูล PostgreSQL
- **ระบบอัตโนมัติ**: ใช้ Apache Airflow ในการกำหนดตารางเวลาและติดตามกระบวนการ ETL

## โครงสร้างโครงการ

capstone-aqi-project/
1. dags/                          # โฟลเดอร์เก็บไฟล์ DAG ของ Airflow
│   1.1 aqi_etl_pipeline.py       # DAG หลักสำหรับดึงข้อมูล ตรวจสอบข้อมูล โหลดข้อมูล
2. sql/                           # โฟลเดอร์เก็บ SQL Queries
│   2.1 create_tables.sql         # คำสั่งสร้างตารางใน PostgreSQL
│   2.2 queries.sql               # SQL สำหรับวิเคราะห์ข้อมูล
3. dbt/                           # โฟลเดอร์เก็บไฟล์ dbt สำหรับการแปลงข้อมู
4. docker-compose.yml             # ไฟล์ตั้งค่า Docker
5. README.md                      # คำอธิบายโปรเจกต์

## การติดตั้ง
### ข้อกำหนดเบื้องต้น
- Docker & Docker Compose
- Apache Airflow
- PostgreSQL

### ขั้นตอนการติดตั้ง
1. คัดลอกโค้ดจาก Repository:
   git clone https://github.com/jiwjiww/capstone-api.git
   cd capstone-api

2. ตั้งค่าตัวแปรสภาพแวดล้อม:
   cp .env.example .env

3. เริ่มต้นระบบด้วย Docker Compose:
   docker-compose up -d

4. เข้าใช้งาน Airflow Web UI:
   - URL: [http://localhost:8080](http://localhost:8080)
   - **ชื่อผู้ใช้เริ่มต้น**: `airflow`
   - **รหัสผ่านเริ่มต้น**: `airflow`

## วิธีการใช้งาน
- DAG `aqi_etl_pipeline.py` จะทำงานอัตโนมัติตามเวลาที่กำหนดไว้ใน Airflow
- สามารถดูบันทึกและรายละเอียดการทำงานได้ผ่าน Airflow UI หรือใช้คำสั่ง CLI:
  airflow dags list
  airflow tasks test aqi_etl_pipeline get_aqi_data 2025-01-01


## กระบวนการทำงานของ Data Pipeline
1. **get_aqi_data**: ดึงข้อมูล AQI จาก API ภายนอกโดยใช้ `requests` และ Airflow `HTTPOperator`
2. **validate_aqi_data**: ทำความสะอาดและแปลงข้อมูลโดยใช้ `pandas`
3. **load_aqi_to_postgres**: โหลดข้อมูลลง PostgreSQL โดยใช้ `PostgreSQL Hook`
4. **PostgreSQL Database**: จัดเก็บข้อมูลที่ผ่านการแปลงแล้วเพื่อการวิเคราะห์

## วิธีตรวจสอบข้อมูลใน PostgreSQL
สามารถใช้คำสั่ง SQL เพื่อตรวจสอบข้อมูลที่โหลดเข้าไปแล้ว:
SELECT * FROM aqi_data LIMIT 10;


## การพัฒนาในอนาคต
- ใช้ **dbt** สำหรับการแปลงข้อมูลเพิ่มเติม เช่น การสร้างตาราง Aggregation หรือ Cleansing Model
- ผสานรวม **Power BI** หรือ **Tableau** สำหรับการแสดงผลข้อมูล
- ขยายการรองรับไปยังเมืองอื่น ๆ

## Troubleshooting
### 1. Airflow Web UI ไม่ทำงาน
- ตรวจสอบสถานะของ container:
  docker-compose ps

- ดู logs ของ Airflow Web Server:
  docker-compose logs airflow-webserver

- ลองรีสตาร์ทบริการ:
  docker-compose restart airflow-webserver


### 2. PostgreSQL ไม่ทำงาน
- ตรวจสอบสถานะของ PostgreSQL container:
  docker-compose ps

- ดู logs:
  docker-compose logs postgres

- ลองรีสตาร์ท:
  docker-compose restart postgres


## ผู้พัฒนา
- **ชวิศา ณ น่าน** ([67130827@dpu.ac.th](mailto:67130827@dpu.ac.th))

## License
โครงการนี้อยู่ภายใต้ลิขสิทธิ์ **MIT License**

