import os

from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold

from db.orm import AsyncORM
from tg_bot.services.state_user import set_command
from tg_bot.services.add_action import add_action

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    try:
        sti = FSInputFile(f"{os.getenv('PROJECT_ROOT')}/src/tg_bot/stickers/5199625264102904058.tgs")
        await message.answer_sticker(sti)

        mess = f"<b>{hbold(message.from_user.first_name)}</b>, вот список доступных команд \n/face\n/body"
        await message.answer(mess, reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        await add_action(message.from_user.id, '/start', action_info=f'{e}')
        await message.answer("Упс... Что-то пошло не так, попробуйте позже")

@router.message(Command("face"))
async def cmd_face(message: Message):
    try:
        set_command(message.from_user.id, "/face")

        await AsyncORM.add_action(message.from_user.id, '/face', None)
        await message.answer("Отправьте фото или видео", reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        await add_action(message.from_user.id, '/face', action_info=f'{e}')
        await message.answer("Упс... Что-то пошло не так, попробуйте позже")

@router.message(Command("body"))
async def cmd_body(message: Message):
    try:
        set_command(message.from_user.id, "/body")

        await AsyncORM.add_action(message.from_user.id, '/body', None)
        await message.answer("Отправьте фото или видео", reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        await add_action(message.from_user.id, '/body', action_info=f'{e}')
        await message.answer("Упс... Что-то пошло не так, попробуйте позже")