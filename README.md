# ระบบดึงข้อมูลคุณภาพอากาศ (Air Quality Data Pipeline)

## ภาพรวม
โครงการนี้เป็นระบบดึงและประมวลผลข้อมูลดัชนีคุณภาพอากาศ (AQI) สำหรับกรุงเทพฯ นนทบุรี และปทุมธานี โดยใช้ Apache Airflow และ PostgreSQL ระบบนี้ช่วยให้สามารถเก็บรวบรวม ทำความสะอาด และจัดเก็บข้อมูลเพื่อการวิเคราะห์ต่อไปได้อย่างอัตโนมัติ

## คุณสมบัติของโครงการ
- **ดึงข้อมูล**: รับข้อมูล AQI จาก API ภายนอก
- **แปลงข้อมูล**: ทำความสะอาดและจัดรูปแบบข้อมูลให้เหมาะสมกับการใช้งาน
- **จัดเก็บข้อมูล**: บันทึกข้อมูลลงในฐานข้อมูล PostgreSQL
- **ระบบอัตโนมัติ**: ใช้ Apache Airflow ในการกำหนดตารางเวลาและติดตามกระบวนการ ETL

## โครงสร้างโครงการ

capstone-aqi-project/
│── dags/                          # โฟลเดอร์เก็บไฟล์ DAG ของ Airflow
│   ├── aqi_etl_pipeline.py        # DAG หลักสำหรับดึงข้อมูล ตรวจสอบข้อมูล โหลดข้อมูล 
│── sql/                           # โฟลเดอร์เก็บ SQL Queries
│   ├── create_tables.sql          # คำสั่งสร้างตารางใน PostgreSQL
│   ├── queries.sql                # SQL สำหรับวิเคราะห์ข้อมูล
│── dbt/                           # ใช้ dbt จะเก็บไฟล์ที่เกี่ยวข้อง
│── docker-compose.yml             # ไฟล์ตั้งค่า Docker 
│── README.md                      # คำอธิบายโปรเจกต์


## การติดตั้ง
### ข้อกำหนดเบื้องต้น
- Docker & Docker Compose
- Apache Airflow
- PostgreSQL

### ขั้นตอนการติดตั้ง
1. คัดลอกโค้ดจาก Repository:  
   git clone https://github.com/your-repo/air-quality-pipeline.git
   cd air-quality-pipeline
   
2. ตั้งค่าตัวแปรสภาพแวดล้อม:
   cp .env.example .env
   
3. เริ่มต้นระบบด้วย Docker Compose: 
   docker-compose up -d

4. เข้าใช้งาน Airflow Web UI:
   - URL: `http://localhost:8080`
   - ชื่อผู้ใช้เริ่มต้น: `airflow/airflow`

## วิธีการใช้งาน
- DAG `aqi_etl_pipeline.py` จะทำงานอัตโนมัติตามเวลาที่กำหนดไว้ใน Airflow
- สามารถดูบันทึกและรายละเอียดการทำงานได้ผ่าน Airflow UI

## กระบวนการทำงานของ Data Pipeline
1. **get_aqi_data**: ดึงข้อมูล AQI จาก API ภายนอก
2. **validate_aqi_data**: ทำความสะอาดและแปลงข้อมูลดิบ
3. **load_aqi_to_postgres**: โหลดข้อมูล
4. **PostgreSQL Database**: จัดเก็บข้อมูลที่ผ่านการแปลงแล้วเพื่อการวิเคราะห์

## เทคโนโลยีที่ใช้
- Apache Airflow
- Python
- PostgreSQL
- Docker

## การพัฒนาในอนาคต
- ใช้ dbt สำหรับการแปลงข้อมูลเพิ่มเติม
- ผสานรวมเครื่องมือแสดงผลข้อมูล
- ขยายการรองรับไปยังเมืองอื่น ๆ

## ผู้พัฒนา
- คุณชวิศา ณ น่าน([67130827@dpu.ac.th](mailto:67130827@dpu.ac.th))
