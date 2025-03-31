import json
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago
from datetime import timedelta

DAG_FOLDER = "/opt/airflow/dags"
API_URL = "https://api.airvisual.com/v2/city"
API_KEY = Variable.get("airvisual_api_key", default_var=None)

if not API_KEY:
    raise ValueError("API key is missing. Set 'airvisual_api_key' in Airflow Variables.")

def _get_aqi_data(city, state, country, **kwargs):
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    
    payload = {"city": city, "state": state, "country": country, "key": API_KEY}
    logging.info(f"Fetching AQI data with params: {payload}")
    response = session.get(API_URL, params=payload, timeout=10)
    
    try:
        data = response.json()
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON response from API: {response.text}")
    
    if response.status_code == 200 and data.get("status") == "success":
        file_path = f"{DAG_FOLDER}/aqi_data_{city.replace(' ', '_')}.json"
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    else:
        raise ValueError(f"API Error {response.status_code}: {data.get('data', {}).get('message', 'Unknown error')}")

def _validate_aqi_data(city, **kwargs):
    file_path = f"{DAG_FOLDER}/aqi_data_{city.replace(' ', '_')}.json"
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        if data.get("status") != "success" or "data" not in data:
            raise ValueError(f"Invalid data for {city}: {data}")
    except Exception as e:
        raise ValueError(f"Error validating data for {city}: {str(e)}")

def _create_aqi_table():
    pg_hook = PostgresHook(postgres_conn_id="postgres_default", schema="aqi_project")
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute("CREATE SCHEMA IF NOT EXISTS aqi_project;")
    cursor.execute("SET search_path TO aqi_project;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aqi_data (
            id SERIAL PRIMARY KEY,
            city TEXT NOT NULL,
            aqi_value INTEGER,
            timestamp TIMESTAMP NOT NULL
        );
    """)
    connection.commit()
    cursor.close()
    connection.close()

def _load_aqi_to_postgres(city, **kwargs):
    pg_hook = PostgresHook(postgres_conn_id="postgres_default", schema="aqi_project")
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    
    file_path = f"{DAG_FOLDER}/aqi_data_{city.replace(' ', '_')}.json"
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        aqi_value = data["data"]["current"]["pollution"].get("aqius", None)
        timestamp = data["data"]["current"]["pollution"].get("ts", None)
        if aqi_value is None or timestamp is None:
            raise ValueError(f"Missing AQI data for {city}: {data}")
        sql = "INSERT INTO aqi_data (city, aqi_value, timestamp) VALUES (%s, %s, %s);"
        cursor.execute(sql, (city, aqi_value, timestamp))
        connection.commit()
    except Exception as e:
        raise ValueError(f"Error inserting data for {city}: {e}")
    finally:
        cursor.close()
        connection.close()

with DAG(
    dag_id="aqi_etl_pipeline",
    schedule_interval="0 0 * * *",
    start_date=days_ago(1),
    catchup=False,
    concurrency=5,
    max_active_runs=1,
    tags=["capstone", "aqi"],
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    create_aqi_table_task = PythonOperator(
        task_id="create_aqi_table",
        python_callable=_create_aqi_table,
        retries=3,
        retry_delay=timedelta(minutes=5)
    )

    cities = [
        {"city": "Bangkok", "state": "Bangkok", "country": "Thailand"},
        {"city": "Nakhon Pathom", "state": "Nakhon Pathom", "country": "Thailand"},
        {"city": "Pathum Thani", "state": "Pathum Thani", "country": "Thailand"}
    ]

    with TaskGroup("aqi_tasks_group") as aqi_tasks_group:
        for city_info in cities:
            city_name = city_info["city"]
            city_normalized = city_name.replace(" ", "_")

            get_aqi_data_task = PythonOperator(
                task_id=f"get_aqi_data_{city_normalized}",
                python_callable=_get_aqi_data,
                op_args=[city_info["city"], city_info["state"], city_info["country"]],
                retries=3,
                retry_delay=timedelta(minutes=3)
            )

            validate_aqi_data_task = PythonOperator(
                task_id=f"validate_aqi_data_{city_normalized}",
                python_callable=_validate_aqi_data,
                op_args=[city_name],
                retries=3,
                retry_delay=timedelta(minutes=3)
            )

            load_aqi_to_postgres_task = PythonOperator(
                task_id=f"load_aqi_to_postgres_{city_normalized}",
                python_callable=_load_aqi_to_postgres,
                op_args=[city_name],
                retries=3,
                retry_delay=timedelta(minutes=3)
            )

            get_aqi_data_task >> validate_aqi_data_task >> load_aqi_to_postgres_task

    start >> create_aqi_table_task >> aqi_tasks_group >> end