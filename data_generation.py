import os

from pymongo import MongoClient
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv

load_dotenv()
ip = os.getenv('IP')
user = os.getenv('USER')
password = os.getenv('PASSWORD')

# Подключение к локальному серверу MongoDB
client = MongoClient(f"mongodb://{user}:{password}@{ip}27017/")
db = client["analytics_db"]

# Функция генерации случайных данных
def random_date(days=30):
    return datetime.utcnow() - timedelta(days=random.randint(0, days))

# 1. UserSessions
user_sessions = db["UserSessions"]
user_sessions.insert_many([
    {
        "session_id": f"sess_{i}",
        "user_id": f"user_{random.randint(1, 100)}",
        "start_time": random_date(),
        "end_time": random_date(),
        "pages_visited": [f"page_{random.randint(1, 10)}" for _ in range(random.randint(1, 5))],
        "device": random.choice(["mobile", "desktop", "tablet"]),
        "actions": [f"action_{random.randint(1, 5)}" for _ in range(random.randint(1, 5))]
    }
    for i in range(10)
])

# 2. ProductPriceHistory (История цен)
product_prices = db["ProductPriceHistory"]
product_prices.insert_many([
    {
        "product_id": f"prod_{i}",
        "price_changes": [{"date": random_date(), "price": round(random.uniform(10, 100), 2)} for _ in range(5)],
        "current_price": round(random.uniform(10, 100), 2),
        "currency": "USD"
    }
    for i in range(10)
])

# 3. EventLogs (Логи событий)
event_logs = db["EventLogs"]
event_logs.insert_many([
    {
        "event_id": f"event_{i}",
        "timestamp": random_date(),
        "event_type": random.choice(["click", "view", "purchase", "error"]),
        "details": "Some event details"
    }
    for i in range(10)
])

# 4. SupportTickets (Обращения в поддержку)
support_tickets = db["SupportTickets"]
support_tickets.insert_many([
    {
        "ticket_id": f"ticket_{i}",
        "user_id": f"user_{random.randint(1, 100)}",
        "status": random.choice(["open", "closed", "pending"]),
        "issue_type": random.choice(["billing", "technical", "general"]),
        "messages": ["Message 1", "Message 2"],
        "created_at": random_date(),
        "updated_at": random_date()
    }
    for i in range(10)
])

# 5. UserRecommendations (Рекомендации пользователям)
user_recommendations = db["UserRecommendations"]
user_recommendations.insert_many([
    {
        "user_id": f"user_{i}",
        "recommended_products": [f"prod_{random.randint(1, 20)}" for _ in range(5)],
        "last_updated": random_date()
    }
    for i in range(10)
])

# 6. ModerationQueue (Очередь модерации отзывов)
moderation_queue = db["ModerationQueue"]
moderation_queue.insert_many([
    {
        "review_id": f"review_{i}",
        "user_id": f"user_{random.randint(1, 100)}",
        "product_id": f"prod_{random.randint(1, 20)}",
        "review_text": "Some review text",
        "rating": random.randint(1, 5),
        "moderation_status": random.choice(["pending", "approved", "rejected"]),
        "flags": ["spam", "offensive"] if random.random() > 0.7 else [],
        "submitted_at": random_date()
    }
    for i in range(10)
])

# 7. SearchQueries (Поисковые запросы)
search_queries = db["SearchQueries"]
search_queries.insert_many([
    {
        "query_id": f"query_{i}",
        "user_id": f"user_{random.randint(1, 100)}",
        "query_text": f"search_{random.randint(1, 50)}",
        "timestamp": random_date(),
        "filters": {"category": random.choice(["electronics", "books", "clothing"]), "price_range": "10-50"},
        "results_count": random.randint(0, 100)
    }
    for i in range(10)
])

print("MongoDB database populated successfully!")
