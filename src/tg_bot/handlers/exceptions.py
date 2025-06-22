from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.enums import ContentType
from tg_bot.services.state_user import get_last_command
from db.orm import AsyncORM
from tg_bot.services.add_action import add_action

router = Router()

@router.message(F.content_type.in_({ContentType.TEXT, ContentType.DOCUMENT, ContentType.VOICE, ContentType.AUDIO}))
async def unsupported_content(message: Message):
    try:
        if not get_last_command(message.from_user.id):
            await message.answer("Сначала выберите команду: /face или /body")
        else:
            await AsyncORM.add_action(message.from_user.id, 'write text', message.text)
            await message.answer("Отправьте фото или видео", reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        await add_action(message.from_user.id, 'unsupported content', action_info=f'{e}')
        await message.answer("Упс... Что-то пошло не так, попробуйте позже")


