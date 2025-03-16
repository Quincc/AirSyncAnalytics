from airflow import DAG
from airflow.operators.python import PythonOperator
from pymongo import MongoClient
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
ip = os.getenv('IP')
user = os.getenv('USER')
password = os.getenv('PASSWORD')


# Параметры подключения
MONGO_URI = f"mongodb://{ip}:27017/"
POSTGRES_CONN = {
    "dbname": "analytics_db",
    "user": f"{user}",
    "password": f"{password}",
    "host": f"{ip}",
    "port": "5432"
}


# Функция для переноса данных из MongoDB в PostgreSQL
def transfer_collection(collection_name, table_name, transform_func=None):
    client = MongoClient(MONGO_URI)
    mongo_db = client["analytics_db"]
    pg_conn = psycopg2.connect(**POSTGRES_CONN)
    pg_cursor = pg_conn.cursor()

    data = list(mongo_db[collection_name].find())

    if not data:
        print(f"No data found in {collection_name}")
        return

    # Преобразуем данные, если есть функция transform_func
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
    "start_date": datetime(2024, 3, 16),
}

dag = DAG(
    "mongo_to_postgres", default_args=default_args, schedule_interval="@daily"
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
