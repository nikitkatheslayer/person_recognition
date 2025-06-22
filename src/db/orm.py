from db.database import Base, async_engine, async_session
from db.models import Users, TgUsers, TgActions
from sqlalchemy import select

class AsyncORM:
    @staticmethod
    async def create_tables():
        print("Создание таблиц...")
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        async_engine.echo = True
        await async_engine.dispose()
        print("Готово.")

    @staticmethod
    async def add_tg_user(id: int, username: str, first_name: str, last_name: str, phone_number: int):
        async with async_session() as session:
            new_tg_user = TgUsers(
                id=id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                is_active=True
            )
            session.add(new_tg_user)
            await session.commit()
            return new_tg_user

    @staticmethod
    async def add_action(tg_users_id: int, action: str, action_info):
        async with async_session() as session:
            new_tg_action = TgActions(
                tg_users_id=tg_users_id,
                action=action,
                action_info=action_info
            )
            session.add(new_tg_action)
            await session.commit()
            return new_tg_action

    @staticmethod
    async def get_all_tg_users():
        async with async_session() as session:
            query = select(TgUsers)
            # print(query.compile(compile_kwargs={"literal_binds": True}))
            res = await session.execute(query)
            result = res.scalars().all()
            return result

    @staticmethod
    async def get_tg_user(username):
        async with async_session() as session:
            query = (
                select(
                    TgUsers
                )
                .where(TgUsers.username == username)
            )
            # print(query.compile(compile_kwargs={"literal_binds": True}))
            res = await session.execute(query)
            result = res.scalars().all()
            return result

    @staticmethod
    async def get_user_photo(photo):
        async with async_session() as session:
            query = (
                select(
                    Users
                )
                .where(Users.photo == photo)
            )
            # print(query.compile(compile_kwargs={"literal_binds": True}))
            res = await session.execute(query)
            result = res.scalars().all()
            return result