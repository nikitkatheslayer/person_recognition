import os
from aiogram.types import Message, FSInputFile
from aiogram import Router, types, F, Bot

from tg_bot.keyboards.for_photo import get_button_ident
from tg_bot.services.state_user import get_last_command, set_user_path
from tg_bot.services.file import save_file, get_file
from tg_bot.services.add_action import add_action
from tg_bot.services.AI import recognize_face_video, recognize_person_video

router = Router()

@router.message(F.video)
async def video_handler(message: Message, bot: Bot):
    try:
        last_command = get_last_command(message.from_user.id)
        video_id = message.video.file_id
        user = message.from_user.id

        if last_command == "/face":
            await process_face(message, bot, video_id, user)
        elif last_command == "/body":
            await process_body(message, bot, video_id, user)
        else:
            await message.answer("Сначала выберите команду: /face или /body")
    except Exception as e:
        await add_action(message.from_user.id, 'video handler', action_info=f'{e}')
        await message.answer("Упс... Что-то пошло не так, попробуйте позже")

async def process_face(message: Message, bot: Bot, video_id: str, user: int):
    try:
        await message.answer("Идёт обработка видео⏳", reply_markup=types.ReplyKeyboardRemove())

        video_path, file_name, file_ext = await save_file(bot, user, video_id, 'video')

        await add_action(user, 'download video for recognize', file_id=video_id, file_ext=file_ext, is_result=False)

        time_detected, dir_path, width, height = recognize_face_video(video_path)
        set_user_path(user, dir_path)

        await message.answer("Отправляю вам видео...")

        detected_file_path = get_file('video', video_id, file_ext)
        detected_video = FSInputFile(detected_file_path)

        await message.answer_video(detected_video, width=width, height=height)
        await message.answer(f"Я обнаружил количество образов человека равным {len(time_detected)}")
        for time in time_detected:
            await message.answer(f"Время обнаружения для ID: {time['id']} - {time['time_detected']} секунда")
        await message.answer("Можете отправить еще что-нибудь, либо выполнить идентификацию", reply_markup=get_button_ident())
        await add_action(user, 'result recognize face', file_id=video_id, file_ext=file_ext, is_result=True)
    except Exception as e:
        await add_action(message.from_user.id, 'process face video', action_info=f'{e}')
        await message.answer("Упс... Что-то пошло не так, попробуйте позже")

async def process_body(message: Message, bot: Bot, video_id: str, user: int):
    try:
        await message.answer("Идёт обработка видео⏳", reply_markup=types.ReplyKeyboardRemove())

        video_path, file_name, file_ext = await save_file(bot, user, video_id, 'video')

        await add_action(user, 'download video for recognize', file_id=video_id, file_ext=file_ext, is_result=False)

        person_count, width, height = recognize_person_video(video_path)

        await message.answer("Отправляю вам видео...")

        detected_file_path = get_file('video', video_id, file_ext)
        detected_video = FSInputFile(detected_file_path)

        await message.answer_video(detected_video, width=width, height=height)
        await message.answer(f"Количество образов на видео: {person_count}")

        await message.answer("Отправляю вам файл с результатом...")

        detected_json_path = get_file('video', 'result', '.json', is_source=True)
        detected_json = FSInputFile(detected_json_path)

        await message.answer_document(detected_json)
        await message.answer("Можете отправить еще что-нибудь")
        await add_action(user, 'result recognize body', file_id=video_id, file_ext=file_ext, is_result=True)
    except Exception as e:
        await add_action(message.from_user.id, 'process body video', action_info=f'{e}')
        await message.answer("Упс... Что-то пошло не так, попробуйте позже")