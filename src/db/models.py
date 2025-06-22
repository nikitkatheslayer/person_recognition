from datetime import datetime
from typing import Annotated
from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow)]

class TgUsers(Base):
    __tablename__ = "tg_users"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=True)
    start_date: Mapped[created_at]

class TgActions(Base):
    __tablename__ = "tg_actions"

    id: Mapped[intpk]
    tg_users_id: Mapped[int] = mapped_column(ForeignKey("tg_users.id"))
    action: Mapped[str] = mapped_column(nullable=True)
    action_info: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[created_at]

class Users(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    service_number: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    patronymic: Mapped[str] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(nullable=True)
    age: Mapped[int] = mapped_column(nullable=True)
    birth_date: Mapped[datetime] = mapped_column(nullable=True)
    birth_place: Mapped[str] = mapped_column(nullable=True)
    photo: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]