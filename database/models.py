from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func
from database.connection import engine
from datetime import datetime

class Base(DeclarativeBase):
    pass

class UrlModel(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

    responses: Mapped[list["ResponseModel"]] = relationship()


class ResponseModel(Base):
    __tablename__ = "responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("urls.id", ondelete="cascade"), index=True)
    status_code: Mapped[int]
    response_time: Mapped[int]
    check_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)


async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)