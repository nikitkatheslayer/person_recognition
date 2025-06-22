import os

from aiogram import Router, types, F
from aiogram.types import FSInputFile, CallbackQuery
from aiogram.utils.markdown import hbold

from db.orm import AsyncORM
from tg_bot.keyboards.for_reg import get_button_phone
from tg_bot.services.add_action import add_action

router = Router()

@router.callback_query(F.data == 'start')
async def start_callback_handler(callback: CallbackQuery):

    sti = FSInputFile(f"{os.getenv('PROJECT_ROOT')}/src/tg_bot/stickers/5199625264102904058.tgs")
    await callback.message.answer_sticker(sti)

    mess = f"<b>{hbold(callback.from_user.first_name)}</b>, вот список доступных команд \n/face\n/body"
    await callback.message.answer(mess, reply_markup=types.ReplyKeyboardRemove())

    await callback.answer(text="Спасибо, что воспользовались ботом!")

@router.callback_query(F.data == 'reg')
async def reg_callback_handler(callback: CallbackQuery):
    try:
        check_user = await AsyncORM.get_tg_user(callback.message.from_user.username)
        if not check_user:
            await callback.message.answer(
                f"Пожалуйста, отправьте контакт, используя кнопку\n\n{hbold('Поделиться номером телефона')}",
                reply_markup=get_button_phone()
            )
            await callback.answer()
            return

        mess = f"<b>{hbold(callback.message.from_user.first_name)}</b>, вы уже зарегистрированы!"
        await callback.message.answer(mess, reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        await add_action(callback.message.from_user.id, '/reg', action_info=f'{e}')
        await callback.message.answer("Упс... Что-то пошло не так, попробуйте позже")