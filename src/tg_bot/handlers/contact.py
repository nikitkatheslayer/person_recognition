from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from db.orm import AsyncORM
from tg_bot.keyboards.for_start import get_button_start
from tg_bot.services.add_action import add_action

router = Router()

@router.message(F.contact)
async def contact_handler(message: Message):
    try:
        await AsyncORM.add_tg_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            message.contact.phone_number
        )

        await message.reply("Спасибо, вы зарегистрированы!", reply_markup=types.ReplyKeyboardRemove())
        await add_action(message.from_user.id, 'registration user', action_info=None)
        await message.answer(f"Нажмите на кнопку {hbold('Начать')} для запуска бота", reply_markup=get_button_start())
    except Exception as e:
        await add_action(message.from_user.id, 'registration user', action_info=f'{e}')
        await message.answer("Упс... Что-то пошло не так, попробуйте позже")
