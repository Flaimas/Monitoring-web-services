from database.models import UrlModel
from database.connection import session_factory
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

class AsyncORM:
    @staticmethod
    async def add_url(host: str, title: str):
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
    async def get_all_urls():
        async with session_factory() as session:
            try:
                query = select(UrlModel)
                result = await session.execute(query)
                return result.scalars().all()
            except Exception as e:
                print(f"Не удалось загузить ссылки.")
                return None
    
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