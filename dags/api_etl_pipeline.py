import json
import requests
import certifi

from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils import timezone
from datetime import datetime

DAG_FOLDER = "/opt/airflow/dags"

# URL ของ API
API_URL = "https://api.airvisual.com/v2/city"

# ดึง API Key จาก Airflow Variables
API_KEY = Variable.get("airvisual_api_key")

# พารามิเตอร์สำหรับ API Request
PAYLOAD = {
    "city": "Bangkok",
    "state": "Bangkok",
    "country": "Thailand",
    "key": API_KEY
}


def _get_aqi_data():
    response = requests.get(API_URL, params=PAYLOAD, verify=certifi.where())
    print(f"API URL: {response.url}")  # ดู URL ที่ใช้ request
    print(f"Response Status Code: {response.status_code}")  # ดู status code
    print(f"Response Text: {response.text}")  # ดูข้อมูลดิบที่ API ส่งมา

    data = response.json()
    print(f"Parsed JSON: {json.dumps(data, indent=2)}")  # ดูข้อมูลแบบ JSON

    with open(f"{DAG_FOLDER}/aqi_data.json", "w") as f:
        json.dump(data, f)


import logging

def _validate_aqi_data():
    with open(f"{DAG_FOLDER}/aqi_data.json", "r") as f:
        data = json.load(f)

    logging.info(f"Received data: {json.dumps(data, indent=2)}")

    # ตรวจสอบว่ามี key "data" หรือไม่
    if "data" not in data:
        raise ValueError("Missing 'data' key in response. Check API response.")

    # ตรวจสอบว่ามี key "current" หรือไม่
    if "current" not in data["data"]:
        raise ValueError("Missing 'current' key in response data.")

    # ตรวจสอบว่ามี key "pollution" หรือไม่
    if "pollution" not in data["data"]["current"]:
        raise ValueError("Missing 'pollution' key in response data.")

    logging.info("AQI data validation passed.")



def _create_aqi_table():
    # สร้างตารางใน PostgreSQL ถ้ายังไม่มี
    pg_hook = PostgresHook(
        postgres_conn_id="postgres_default",
        schema="aqi_project"
    )
    connection = pg_hook.get_conn()
    cursor = connection.cursor()

    # สร้างตาราง aqi_data
    sql_aqi_data = """
        CREATE TABLE IF NOT EXISTS aqi_data (
            id SERIAL PRIMARY KEY,
            city TEXT NOT NULL,
            aqi_value INTEGER NOT NULL,
            timestamp TIMESTAMP NOT NULL
        );
    """
    cursor.execute(sql_aqi_data)

    # สร้างตาราง location
    sql_location = """
        CREATE TABLE IF NOT EXISTS location (
            city TEXT PRIMARY KEY,
            Country TEXT NOT NULL
        );
    """
    cursor.execute(sql_location)
    connection.commit()


def _load_aqi_to_postgres():
    # โหลดข้อมูล AQI ลง PostgreSQL
    pg_hook = PostgresHook(
        postgres_conn_id="postgres_default",
        schema="aqi_project"
    )
    connection = pg_hook.get_conn()
    cursor = connection.cursor()

    with open(f"{DAG_FOLDER}/aqi_data.json", "r") as f:
        data = json.load(f)

    city = "Bangkok"
    aqi_value = data["data"]["current"]["pollution"]["aqius"]
    timestamp = data["data"]["current"]["pollution"]["ts"]

    sql = """
        INSERT INTO aqi_data (city, aqi_value, timestamp) 
        VALUES (%s, %s, %s);
    """
    cursor.execute(sql, (city, aqi_value, timestamp))
    connection.commit()

with DAG(
    dag_id="test_postgres_connection",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    check_db = BashOperator(
        task_id="check_postgres_db",
        bash_command="PGPASSWORD='postgres' psql -U postgres -h db -p 5432 -d postgres -c '\l'"
    )

    check_db


# สร้าง DAG สำหรับดึงและโหลด AQI Data
with DAG(
    "aqi_etl_pipeline",
    schedule="0 0 * * *",  # รันทุกวันเวลาเที่ยงคืน
    start_date=timezone.datetime(2025, 2, 1),
    tags=["capstone", "aqi"],
) as dag:

    start = EmptyOperator(task_id="start")

    get_aqi_data = PythonOperator(
        task_id="get_aqi_data",
        python_callable=_get_aqi_data,
    )

    validate_aqi_data = PythonOperator(
        task_id="validate_aqi_data",
        python_callable=_validate_aqi_data,
    )

    create_aqi_table = PythonOperator(
        task_id="create_aqi_table",
        python_callable=_create_aqi_table,
    )

    load_aqi_to_postgres = PythonOperator(
        task_id="load_aqi_to_postgres",
        python_callable=_load_aqi_to_postgres,
    )

    end = EmptyOperator(task_id="end")

    # Workflow Execution
    start >> get_aqi_data >> validate_aqi_data >> load_aqi_to_postgres >> end
    start >> create_aqi_table >> load_aqi_to_postgres

