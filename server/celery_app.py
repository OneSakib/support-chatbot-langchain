from celery import Celery

celery_app = Celery(
    "support_chatbot",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)
