# 📌 Проект: ETL-пайплайн с Apache Airflow, PostgreSQL и MongoDB

## 📌 Описание проекта
Данный проект представляет собой **ETL-процесс**, реализованный с помощью **Apache Airflow**, **PostgreSQL** и **MongoDB**. В рамках проекта настроена **репликация данных** из MongoDB в PostgreSQL, а также построены **аналитические витрины** для анализа пользовательской активности и эффективности службы поддержки.

---
## 🛠 Используемые технологии
- **Apache Airflow** – для автоматизации ETL-процессов.
- **MongoDB** – хранение исходных данных (NoSQL).
- **PostgreSQL** – для аналитики и хранения структурированных данных.
- **Python** – написание DAGs для Airflow.
- **Docker (по желанию)** – развертывание инфраструктуры.

---
## 📂 Структура проекта
```
📁 airflow/
 ├── dags/
 │   ├── replication_dag.py        # DAG для репликации данных из MongoDB в PostgreSQL
 │   ├── update_analytics_dag.py   # DAG для обновления аналитических витрин
📁 database/
 ├── schema_postgres.sql           # Создание таблиц в PostgreSQL
 ├── create_showcases_postgres.sql # Создание аналитических витрин в PostgreSQL
📁 scripts/
 ├── data_generation.py            # Генерация тестовых данных
📁 docs/
 ├── README.md                     # Этот файл
```

---
## 📝 Описание процессов

### **1️⃣ Генерация данных**
- Создаются коллекции в **MongoDB**:
  - `UserSessions` – сессии пользователей.
  - `ProductPriceHistory` – история изменения цен.
  - `EventLogs` – логи событий.
  - `SupportTickets` – обращения в поддержку.
  - `UserRecommendations` – рекомендации.
  - `ModerationQueue` – модерация отзывов.
  - `SearchQueries` – поисковые запросы.

🔹 **Файл**:
- `data_generation.py` – генерация тестовых данных.

### **2️⃣ Репликация данных в PostgreSQL**
- Данные из **MongoDB** переносятся в **PostgreSQL** с использованием **Airflow DAG (`replication_dag.py`)**.
- Обрабатываются:
  - `ObjectId` → `string`
  - `datetime` → `ISO 8601`
  - `lists` → `PostgreSQL ARRAY`

🔹 **Файл**: `replication_dag.py`

### **3️⃣ Создание аналитических витрин**
- Витрина **`user_activity_summary`** – анализирует активность пользователей.
- Витрина **`support_performance`** – анализирует эффективность службы поддержки.
- DAG **`update_analytics_dag.py`** пересчитывает данные ежедневно.

🔹 **Файл**: `update_analytics_dag.py`
🔹 **SQL**:
- `create_showcases_postgres.sql` – скрипт создания аналитических витрин.

---
## 🚀 Запуск проекта
### **1️⃣ Установка зависимостей**
```bash
pip install -r requirements.txt
```

### **2️⃣ Запуск Airflow**
```bash
export AIRFLOW_HOME=~/airflow
airflow db init
airflow scheduler &
airflow webserver -p 8080 &
```

### **3️⃣ Запуск пайплайнов**
Перейти в **Airflow UI** (`http://localhost:8080`):
- Запустить `replication_dag`
- Запустить `update_analytics_dag`

---
## 📊 Анализ данных
- **ТОП-5 активных пользователей:**
  ```sql
  SELECT user_id, total_sessions, total_pages_visited, total_actions
  FROM user_activity_summary
  ORDER BY total_sessions DESC
  LIMIT 5;
  ```
- **Среднее время обработки тикетов:**
  ```sql
  SELECT AVG(avg_resolution_time) AS avg_ticket_time FROM support_performance;
  ```

---
## 📌 Оценочные критерии
✅ Развёрнуты базы данных (MongoDB, PostgreSQL)
✅ Реализована репликация с помощью Airflow
✅ Данные очищены и поддаются аналитике
✅ Построены аналитические витрины
✅ Настроены DAGs в Airflow
✅ Описан процесс в документации

---
## 🏆 Итог
Этот проект представляет собой **полноценный ETL-конвейер**, который **автоматизирует сбор, трансформацию и анализ данных**.

🚀 **Готов к развертыванию и масштабированию!**

