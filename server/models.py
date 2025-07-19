from pydantic import BaseModel

from typing import Dict


class UrlProcessRequest(BaseModel):
    url: str


class UrlProcessResponse(BaseModel):
    task_id: str
    project_id: str


class TaskStatusRequest(BaseModel):
    task_id: str


class TaskStatusResponse(BaseModel):
    state: str
    task_id: str
    result: str | None | Dict


class ChatRequest(BaseModel):
    project_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
