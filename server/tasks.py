# tasks.py
from celery_app import celery_app
from utils.scraper import scrape_website
from utils.embedding import store_embeddings


@celery_app.task
def process_url_task(url: str, project_id: str):
    texts = scrape_website(url)
    store_embeddings(texts, project_id)
    return {"status": "completed", "pages": len(texts)}
