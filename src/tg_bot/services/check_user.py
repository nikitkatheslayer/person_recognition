from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Awaitable, Dict, Any

from tg_bot.keyboards.for_reg import get_button_reg
from db.orm import AsyncORM

class CheckUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Разрешаем /reg без проверки
        if event.text == "/reg":
            return await handler(event, data)
        if event.contact:
            return await handler(event, data)

        # Проверяем пользователя в базе
        user = await AsyncORM.get_tg_user(event.from_user.username)
        if not user:
            await event.answer("Пожалуйста, начните с регистрации", reply_markup=get_button_reg())
            return  # прерываем обработку

        return await handler(event, data)
