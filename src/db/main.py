import asyncio
from datetime import datetime
from db.orm import AsyncORM

async def add_tg_user_orm():
    await AsyncORM.add_tg_user(123456789, "johndoe", "John", "Doe")

async def add_user_orm():
    await AsyncORM.add_user(
        service_number="12345",
        last_name="Иванов",
        firs_name="Иван",
        patronymic="Иванович",
        gender="Мужчина",
        age=30,
        birth_date=datetime(1995, 5, 17),
        birth_place="Москва",
        photo="http://example.com/photo.jpg"
    )

async def get_all_tg_users_orm(username):
    tg_users = await AsyncORM.get_all_tg_users()
    print("tg_users:", tg_users)


async def get_tg_user_orm(username):
    users = await AsyncORM.get_tg_user(username)
    if not users:
        print('NONE')
    for tg in users:
        print("users:", tg.tg_username)


async def get_users_orm():
    users = await AsyncORM.get_all_users()
    print("users:", users)

asyncio.run(AsyncORM.create_tables())
