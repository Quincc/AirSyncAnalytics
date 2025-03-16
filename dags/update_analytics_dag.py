from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 3, 16),
    "catchup": False,
    "retries": 1,
}

dag = DAG(
    "update_analytics_dag",
    default_args=default_args,
    schedule_interval="@daily",
)

def update_user_activity():
    postgres = PostgresHook(postgres_conn_id="postgres_conn")
    sql = """
        DELETE FROM user_activity_summary;
        INSERT INTO user_activity_summary
        SELECT
            user_id,
            COUNT(session_id) AS total_sessions,
            AVG(EXTRACT(EPOCH FROM (end_time - start_time))) AS avg_session_duration,
            SUM(array_length(pages_visited, 1)) AS total_pages_visited,
            SUM(array_length(actions, 1)) AS total_actions
        FROM UserSessions
        GROUP BY user_id;
    """
    postgres.run(sql)

def update_support_performance():
    postgres = PostgresHook(postgres_conn_id="postgres_conn")
    sql = """
        DELETE FROM support_performance;
        INSERT INTO support_performance
        SELECT
            user_id,
            COUNT(ticket_id) AS total_tickets,
            AVG(EXTRACT(EPOCH FROM (updated_at - created_at))) AS avg_resolution_time,
            COUNT(CASE WHEN status = 'closed' THEN 1 END) AS closed_tickets,
            AVG(array_length(messages, 1)) AS avg_messages_per_ticket
        FROM SupportTickets
        GROUP BY user_id;
    """
    postgres.run(sql)

update_user_activity_task = PythonOperator(
    task_id="update_user_activity_summary",
    python_callable=update_user_activity,
    dag=dag,
)

update_support_performance_task = PythonOperator(
    task_id="update_support_performance",
    python_callable=update_support_performance,
    dag=dag,
)

update_user_activity_task >> update_support_performance_task  # Определяем порядок выполнения
