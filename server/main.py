from fastapi.exceptions import HTTPException
import os
from fastapi import FastAPI, BackgroundTasks
from tasks import process_url_task
from celery_app import celery_app
from celery.result import AsyncResult
from models import *
from utils.qa import ask_question
import uuid
from utils.helpers import generate_project_id

# from utils.qa import ask


app = FastAPI()


@app.post("/process-url", response_model=UrlProcessResponse)
def url_process(request: UrlProcessRequest):
    project_id = generate_project_id(request.url)
    task = process_url_task.delay(url=request.url, project_id=project_id)
    return UrlProcessResponse(task_id=task.id, project_id=project_id)


@app.get('/task-status/{task_id}', response_model=TaskStatusResponse)
def get_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return TaskStatusResponse(task_id=task_id, state=result.state, result=result.result if result.ready() else None)


@app.post('/chat', response_model=ChatResponse)
def chat(request: ChatRequest):
    list_dir = os.listdir('chroma_store')
    if request.project_id not in list_dir:
        raise HTTPException(status_code=400, detail="Project Id is wrong!")
    result = ask_question(request.message, request.project_id)
    return ChatResponse(response=result)
