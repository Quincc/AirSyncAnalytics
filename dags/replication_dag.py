from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pymongo import MongoClient
from bson import ObjectId
import json
from datetime import datetime
import os

# Подключение к MongoDB через Airflow Connection
from airflow.hooks.base import BaseHook

mongo_conn = BaseHook.get_connection("mongo_conn")
MONGO_URI = f"mongodb://{mongo_conn.login}:{mongo_conn.password}@{mongo_conn.host}:{mongo_conn.port}/"


# Функция для преобразования ObjectId, datetime, списков и JSON
def clean_data(doc):
    doc.pop("_id", None)  # Удаляем _id, если он есть
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)  # Преобразуем ObjectId в строку
        elif isinstance(value, datetime):
            doc[key] = value.isoformat()  # Преобразуем datetime в строку ISO 8601
        elif isinstance(value, dict):  # Преобразуем вложенные JSON в JSON-строки
            doc[key] = json.dumps(value, ensure_ascii=False, default=str)
        elif isinstance(value, list):
            if len(value) == 0:
                doc[key] = "{}"  # PostgreSQL требует {} для пустых массивов
            elif all(isinstance(item, dict) for item in value):
                doc[key] = json.dumps(value, ensure_ascii=False, default=str)  # JSON-строка
            elif all(isinstance(item, (str, int, float, bool)) for item in value):
                doc[key] = "{" + ",".join(f'"{str(item)}"' for item in value) + "}"  # PostgreSQL ARRAY
            else:
                doc[key] = json.dumps(value, ensure_ascii=False, default=str)  # Прочие списки как JSON
    return doc


# Функция для переноса данных из MongoDB в PostgreSQL
def transfer_collection(collection_name, table_name, transform_func=None):
    client = MongoClient(MONGO_URI)
    mongo_db = client["analytics_db"]

    postgres = PostgresHook(postgres_conn_id="postgres_conn")
    pg_conn = postgres.get_conn()
    pg_cursor = pg_conn.cursor()

    data = list(mongo_db[collection_name].find())

    if not data:
        print(f"No data found in {collection_name}")
        return

    # Преобразуем данные
    data = [clean_data(doc) for doc in data]

    if transform_func:
        data = [transform_func(doc) for doc in data]

    # Генерация SQL запроса
    columns = data[0].keys()
    insert_query = f"""
        INSERT INTO {table_name} ({', '.join(columns)})
        VALUES ({', '.join(['%s'] * len(columns))})
        ON CONFLICT DO NOTHING
    """

    records = [tuple(doc.values()) for doc in data]
    pg_cursor.executemany(insert_query, records)
    pg_conn.commit()
    pg_cursor.close()
    pg_conn.close()
    client.close()
    print(f"Data transferred from {collection_name} to {table_name}")


# DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 3, 16),
    "catchup": False,
    "retries": 1,
}

dag = DAG(
    "replication_dag", default_args=default_args, schedule_interval="@daily"
)

collections_mapping = {
    "UserSessions": "UserSessions",
    "ProductPriceHistory": "ProductPriceHistory",
    "EventLogs": "EventLogs",
    "SupportTickets": "SupportTickets",
    "UserRecommendations": "UserRecommendations",
    "ModerationQueue": "ModerationQueue",
    "SearchQueries": "SearchQueries",
}

# Создаем таски для каждой коллекции
for mongo_collection, pg_table in collections_mapping.items():
    task = PythonOperator(
        task_id=f"transfer_{mongo_collection}",
        python_callable=transfer_collection,
        op_kwargs={"collection_name": mongo_collection, "table_name": pg_table},
        dag=dag,
    )
