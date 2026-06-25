from schemas.urls import UrlCreateSchema
from pydantic import ValidationError
from database.database import AsyncORM
from database.models import UrlModel

async def handle_url_input(raw_url: str, raw_title: str):
    try:
        validated = UrlCreateSchema(url=raw_url, title=raw_title)
        host = str(validated.url.host)
        title = validated.title
    except ValidationError:
        print(f"Ошибка ввода: проверьте правильность URL-адреса {raw_url}.")
        return False
    
    success = await AsyncORM.add_url(host=host, title=title)
    return success

async def handle_url_output(only_active: bool = False) -> list[UrlModel] | None:
    return await AsyncORM.get_all_urls(only_active)

async def handle_get_url_for_id(id: int) -> UrlModel | None:
    return await AsyncORM.get_url_for_id(id)

async def handle_add_response(service_id: int, status_code: int, response_time: float) -> bool:
    return await AsyncORM.add_response(service_id=service_id, status_code=status_code, response_time=response_time)