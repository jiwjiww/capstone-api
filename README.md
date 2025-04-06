# 🌫️ AQI Data Pipeline for Bangkok, Nakhon Pathom, and Pathum Thani

## 🧾 Project Overview
This project is an automated data pipeline for collecting and analyzing daily **Air Quality Index (AQI)** data for Bangkok, Nakhon Pathom, and Pathum Thani using **Apache Airflow**, **PostgreSQL**, **dbt**, and **Streamlit**. The pipeline fetches AQI data from the AirVisual API, transforms and validates it, stores it in a relational database, and visualizes it through an interactive web dashboard.

---

## 🎯 Objectives
1. Fetch daily AQI data from the AirVisual API.
2. Transform and clean the data into an analysis-ready format.
3. Validate data quality.
4. Load cleaned data into PostgreSQL.
5. Use SQL & dbt to model data and answer business questions.
6. Visualize AQI data interactively with Streamlit.

---

## ⚙️ Features
- ⏬ **Automated Data Ingestion** via Airflow DAGs  
- 🧼 **Data Cleaning & Transformation** using Python and dbt  
- 🗄️ **Centralized Storage** in PostgreSQL  
- 📊 **Interactive Dashboards** using Streamlit  
- 📋 **Data Quality Validation**  
- 🧠 **Analytical SQL Queries** and business insights

---

## 📁 Project Structure
```bash
capstone-aqi/
├── dags/                         # Airflow DAGs สำหรับควบคุม ETL pipeline
│   └── aqi_etl_pipeline.py       # DAG หลักสำหรับดึง ตรวจสอบ และโหลดข้อมูล AQI
│
├── sql/                          # คำสั่ง SQL สำหรับสร้างตารางและการวิเคราะห์
│   ├── create_tables.sql         # สคริปต์สำหรับสร้างตารางใน PostgreSQL
│   └── queries.sql               # SQL สำหรับตอบคำถามทางธุรกิจ
│
├── dbt/                          # ไฟล์สำหรับ dbt (data transformation) 
│   ├── models/                   # โฟลเดอร์เก็บ model ต่าง ๆ ที่เขียนด้วย SQL
│   ├── dbt_project.yml           # ไฟล์ตั้งค่าโปรเจกต์ dbt
│   └── profiles.yml              # ไฟล์กำหนดการเชื่อมต่อกับ database สำหรับ dbt
│
├── streamlit_app/                # แอป Streamlit สำหรับสร้าง dashboard
│   └── business_qa_dashboard.py  # ตัวแอปหลักแสดงผล AQI แบบ interactive
│
├── docker-compose.yml            # ไฟล์ตั้งค่าการทำงานร่วมของ Docker containers
├── .env                          # ตัวแปรสภาพแวดล้อม เช่น API keys, DB config
└── README.md                     # เอกสารอธิบายโปรเจกต์


---

## 🚀 Installation & Setup

### 📌 Prerequisites
- Docker & Docker Compose
- Git
- Internet access (for API)

### 🧰 Setup Steps
```bash
# 1. Clone the repository
git clone https://github.com/jiwjiww/capstone-api.git
cd capstone-api

# 2. Configure environment variables
cp .env.example .env

# 3. Start backend services
docker-compose up -d

# 4. (Optional) Run Streamlit app
cd streamlit_app
streamlit run dashboard.py


🌐 Access Airflow
URL: http://localhost:8080
Username: airflow
Password: airflow

🌐 Access Streamlit Dashboard
URL: http://localhost:8501


🔄 ETL Pipeline Workflow (Airflow DAG: aqi_etl_pipeline)
Step	Task ID	               Description
1	   get_aqi_data :	        Retrieve AQI data from external API using requests
2	   validate_aqi_data	:   Clean and validate data using pandas
3	   load_aqi_to_postgres : Load the cleaned data into PostgreSQL
4	   run_dbt_models :       Run dbt to create data models (optional)

🧪 Check Data in PostgreSQL
SELECT * FROM aqi_data LIMIT 10;

📊 Business Questions Answered
1. Which city had the highest AQI during the past week?
2. Which city had the lowest AQI in the past 3 months?
3. What is the average AQI this week for each city?
4. How many days this month did the AQI exceed 100 in each city?
5. What is the daily AQI trend this week across Bangkok, Nakhon Pathom, and Pathum Thani?


📈 Streamlit Dashboard
The business_qa_dashboard.py script inside streamlit_app/ folder allows users to explore AQI trends interactively with:
- Time-series graphs
- Average AQI by city
- Daily and monthly comparisons


🔮 Future Enhancements
- Add support for additional cities in Thailand
- Use Machine Learning for AQI forecasting
- Deploy the Streamlit dashboard on the cloud (e.g., Streamlit Cloud, Heroku, or AWS EC2)
- Add user interactivity to the dashboard (e.g., filters, date ranges, city selection)
- Implement real-time data updates with API integration

🛠 Troubleshooting
❌ Airflow Web UI Not Working
docker-compose ps
docker-compose logs airflow-webserver
docker-compose restart airflow-webserver

❌ PostgreSQL Not Working
docker-compose ps
docker-compose logs postgres
docker-compose restart postgres

❌ Streamlit App Not Running
# Make sure required packages are installed
pip install -r requirements.txt
# Start the app
streamlit run streamlit_app/bisiness_qa_dashboard.py


👩‍💻 Developer
ชวิศา ณ น่าน
📧 67130827@dpu.ac.th