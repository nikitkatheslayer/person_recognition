from aiogram.types import Message, FSInputFile
from aiogram import Router, types, F, Bot

from tg_bot.keyboards.for_photo import get_button_photo, get_button_ident
from tg_bot.services.state_user import get_last_command
from tg_bot.services.file import save_file, get_file
from tg_bot.services.add_action import add_action
from tg_bot.services.AI import recognize_face_photo, recognize_person_photo

router = Router()

@router.message(F.photo)
async def photo_handler(message: Message, bot: Bot):
    try:
        user = message.from_user.id
        image_id = message.photo[-1].file_id
        last_command = get_last_command(user)

        if last_command == "/face":
            await process_face(message, bot, image_id, user)
        elif last_command == "/body":
            await process_body(message, bot, image_id, user)
        else:
            await message.answer("Сначала выберите команду: /face или /body")
    except Exception as e:
        await add_action(message.from_user.id, 'photo handler', action_info=f'{e}')
        await message.answer("Упс... Что-то пошло не так, попробуйте позже")

async def process_face(message: Message, bot: Bot, image_id: str, user: int):
    try:
        await message.answer("Идёт обработка изображения⏳", reply_markup=types.ReplyKeyboardRemove())

        image_path, file_name, file_ext = await save_file(bot, user, image_id, 'image')
        await add_action(user, 'download photo for recognize', file_id=image_id, file_ext=file_ext, is_result=False)

        count_faces = recognize_face_photo(image_path)
        if count_faces < 1:
            await add_action(user, 'result recognize face', file_id=image_id, file_ext=file_ext,
                             action_info='count faces < 1')
            await message.answer("Я ничего не обнаружил, попробуйте другое изображение")
            return

        await message.answer("Отправляю вам изображение...")
        detected_file_path = get_file('image', image_id, file_ext)
        detected_image = FSInputFile(detected_file_path)
        await message.answer_photo(detected_image)
        await message.answer(f"Я обнаружил количество лиц равным {count_faces}")
        await add_action(user, 'result recognize face', file_id=image_id, file_ext=file_ext, is_result=True)

        if count_faces == 1:
            await message.answer("Я могу выполнить следующее:", reply_markup=get_button_photo())
            await message.answer("Либо отправьте, что-нибудь другое")
        else:
            if not image_path:
                await message.answer("Можете отправить еще что-нибудь")
            else:
                await message.answer(
                    "Можете отправить еще что-нибудь, либо выполнить идентификацию",
                    reply_markup=get_button_ident()
                )
    except Exception as e:
        await add_action(message.from_user.id, 'process face photo', action_info=f'{e}')
        await message.answer("Упс... Что-то пошло не так, попробуйте позже")

async def process_body(message: Message, bot: Bot, image_id: str, user: int):
    try:
        await message.answer("Идёт обработка изображения⏳", reply_markup=types.ReplyKeyboardRemove())

        image_path, file_name, file_ext = await save_file(bot, user, image_id, 'image')
        await add_action(user, 'download photo for recognize', file_id=image_id, file_ext=file_ext, is_result=False)

        person_count = recognize_person_photo(image_path)
        if not person_count:
            await add_action(user, 'result recognize person', file_id=image_id, file_ext=file_ext,
                             action_info='not persons')
            await message.answer("Я ничего не обнаружил, попробуйте другое изображение")
            return

        await message.answer("Отправляю вам изображение...")
        detected_file_path = get_file('image', image_id, file_ext)
        detected_photo = FSInputFile(detected_file_path)
        await message.answer_photo(detected_photo)
        await message.answer(f"Я обнаружил количество образов человека равным {person_count}")
        await message.answer("Можете отправить еще что-нибудь")
        await add_action(user, 'result recognize body', file_id=image_id, file_ext=file_ext, is_result=True)
    except Exception as e:
        await add_action(message.from_user.id, 'process body photo', action_info=f'{e}')
        await message.answer("Упс... Что-то пошло не так, попробуйте позже")