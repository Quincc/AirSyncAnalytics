# 📌 Project: ETL Pipeline with Apache Airflow, PostgreSQL, and MongoDB

## 📌 Project Description
This project is an **ETL process** implemented using **Apache Airflow**, **PostgreSQL**, and **MongoDB**. It sets up **data replication** from MongoDB to PostgreSQL and builds **analytical dashboards** to analyze user activity and support service performance.

---
## 🛠 Technologies Used
- **Apache Airflow** – to automate ETL processes.
- **MongoDB** – to store source data (NoSQL).
- **PostgreSQL** – for analytics and storing structured data.
- **Python** – to write DAGs for Airflow.
- **Docker (optional)** – for deploying the infrastructure.

---
## 📂 Project Structure
```
📁 airflow/
 ├── dags/
 │   ├── replication_dag.py        # DAG for data replication from MongoDB to PostgreSQL
 │   ├── update_analytics_dag.py   # DAG for updating analytical dashboards
📁 database/
 ├── schema_postgres.sql           # Table creation in PostgreSQL
 ├── create_showcases_postgres.sql # Analytical dashboards creation in PostgreSQL
📁 scripts/
 ├── data_generation.py            # Test data generation
📁 docs/
 ├── README.md                     # This file
```

---
## 📝 Process Description

### **1️⃣ Data Generation**
- Collections created in **MongoDB**:
  - `UserSessions` – user sessions.
  - `ProductPriceHistory` – price change history.
  - `EventLogs` – event logs.
  - `SupportTickets` – support tickets.
  - `UserRecommendations` – recommendations.
  - `ModerationQueue` – review moderation.
  - `SearchQueries` – search queries.

🔹 **File**:
- `data_generation.py` – generates test data.

### **2️⃣ Data Replication to PostgreSQL**
- Data from **MongoDB** is transferred to **PostgreSQL** using **Airflow DAG (`replication_dag.py`)**.
- Conversions handled:
  - `ObjectId` → `string`
  - `datetime` → `ISO 8601`
  - `lists` → `PostgreSQL ARRAY`

🔹 **File**: `replication_dag.py`

### **3️⃣ Creating Analytical Dashboards**
- Dashboard **`user_activity_summary`** – analyzes user activity.
- Dashboard **`support_performance`** – analyzes support service performance.
- DAG **`update_analytics_dag.py`** recalculates data daily.

🔹 **File**: `update_analytics_dag.py`
🔹 **SQL**:
- `create_showcases_postgres.sql` – script to create dashboards.

---
## 🚀 Project Launch
### **1️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2️⃣ Launch Airflow**
```bash
export AIRFLOW_HOME=~/airflow
airflow db init
airflow scheduler &
airflow webserver -p 8080 &
```

### **3️⃣ Run Pipelines**
Open **Airflow UI** (`http://localhost:8080`):
- Run `replication_dag`
- Run `update_analytics_dag`

---
## 📊 Data Analysis
- **TOP-5 active users:**
  ```sql
  SELECT user_id, total_sessions, total_pages_visited, total_actions
  FROM user_activity_summary
  ORDER BY total_sessions DESC
  LIMIT 5;
  ```
- **Average ticket resolution time:**
  ```sql
  SELECT AVG(avg_resolution_time) AS avg_ticket_time FROM support_performance;
  ```

---
## 📌 Evaluation Criteria
✅ Databases deployed (MongoDB, PostgreSQL)
✅ Replication implemented via Airflow
✅ Data cleaned and ready for analytics
✅ Analytical dashboards built
✅ DAGs configured in Airflow
✅ Process described in documentation

---
## 🏆 Result
This project is a **full-fledged ETL pipeline** that **automates data collection, transformation, and analysis**.

🚀 **Ready for deployment and scaling!**
