from database.models import UrlModel, ResponseModel
from database.connection import session_factory
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

class AsyncORM:
    @staticmethod
    async def add_url(host: str, title: str) -> bool:
        async with session_factory() as session: 
            url_row = UrlModel(
                url=host,
                title=title
            )
            session.add(url_row)

            try:
                await session.commit()
                return True
            except IntegrityError:
                await session.rollback()
                print(f"Хост {host} уже есть в базе.")
                return False
            except Exception as e:
                await session.rollback()
                print(f"Ошибка при работе с БД: {e}")
                return False
    
    @staticmethod
    async def get_all_urls(only_active: bool = False) -> list[UrlModel]:
        async with session_factory() as session:
            query = select(UrlModel)
            if only_active:
                query = query.where(UrlModel.is_active)

            try:
                result = await session.execute(query)
                return result.scalars().all()
            except Exception as e:
                print(f"Не удалось загузить ссылки.")
                return []
    
    @staticmethod
    async def get_url_for_id(id: int):
        async with session_factory() as session:
            try:
                query = select(UrlModel).where(UrlModel.id == id)
                result = await session.execute(query)
                return result.scalar_one_or_none()
            except Exception as e:
                print(f"Не удалось получить ссылку из БД")
                return None
            
    @staticmethod
    async def add_response(service_id: int, status_code: int, response_time: float):
        async with session_factory() as session:
            response = ResponseModel(
                service_id=service_id,
                status_code=status_code,
                response_time=response_time,
            )
            session.add(response)
            try:
                await session.commit()
                return True
            except Exception as e:
                await session.rollback()
                print(f"Ошибка при работе с БД: {e}")
                return False