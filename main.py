from typing import Annotated
import uvicorn
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from database.models import setup_database
from handlers.handlers import handle_url_input, handle_url_output, handle_get_url_for_id
from schemas.urls import UrlResponseSchema
import asyncio


from services.checker import run_monitoring_loop
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Всё, что ДО yield, выполняется ПРИ СТАРТЕ сервера
    # create_task запускает бесконечный цикл в фоне
    bg_task = asyncio.create_task(run_monitoring_loop())
    
    yield  # Здесь FastAPI работает и принимает запросы
    
    # Всё, что ПОСЛЕ yield, выполняется ПРИ ОСТАНОВКЕ сервера
    bg_task.cancel()  # Мягко тушим воркер при выключении приложения

app = FastAPI(lifespan=lifespan)

@app.get("/urls", response_model=list[UrlResponseSchema])
async def get_all_monitoring_urls():
    """
    Эндпоинт возвращает список всех сайтов, стоящих на мониторинге
    """
    return await handle_url_output()

@app.get("/urls/{url_id}")
async def get_url(url_id: int):
    """
    Эндпоинт возвращает сайт по id
    """
    url = await handle_get_url_for_id(url_id)
    if url is None:
        raise HTTPException(status_code=404, detail="Url с таким id не найден")
    return url