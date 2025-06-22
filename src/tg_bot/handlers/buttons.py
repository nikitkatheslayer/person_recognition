import os
from aiogram.types import Message, FSInputFile
from aiogram import Router, types, F

from tg_bot.services.add_action import add_action
from tg_bot.services.state_user import get_last_user_path
from tg_bot.services.AI import identify_face_photo, analyze_face_photo
from tg_bot.services.file import get_file
from db.orm import AsyncORM

router = Router()

@router.message(F.text == 'Идентифицировать🔍')
async def handler_button_ident(message: Message):
    try:
        user = message.from_user.id
        path = get_last_user_path(user)
        await add_action(user, 'identification face', action_info=None)
        await message.answer("Идентифицирую...⏳")

        find_result = []
        if os.path.isdir(path):
            dir_for_ident = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            for image_path in dir_for_ident:
                video_res_path = os.path.join(path, image_path)
                video_res = identify_face_photo(video_res_path)
                find_result.append(video_res)
        else:
            photo_res = identify_face_photo(path)
            find_result.append(photo_res)
        find_result = [res for res in find_result if res is not None]

        if not find_result:
            await message.answer("Я не смог найти такого человека в базе данных")
            await message.answer("Можете отправить еще что-нибудь")
            return
        for ident in list(set(find_result)):
            if ident is not None:
                file_name, file_ext = os.path.splitext(ident)
                user_info = await AsyncORM.get_user_photo(ident)
                await message.answer(f"ФИО: {user_info[0].last_name} {user_info[0].first_name} {user_info[0].patronymic}\n"
                                     f"Табельный номер: {user_info[0].service_number}\n"
                                     f"Пол: {user_info[0].gender}\n"
                                     f"Дата рождения: {user_info[0].birth_date}\n"
                                     f"Возраст: {user_info[0].age}\n")

                detected_file_path = get_file('users', file_name, file_ext, is_source=True)
                detected_photo = FSInputFile(detected_file_path)

                await message.answer_photo(detected_photo)
        await message.answer("Можете отправить еще что-нибудь")
    except Exception as e:
        await add_action(message.from_user.id, 'ident button', action_info=f'{e}')
        await message.answer("Упс... Что-то пошло не так, попробуйте позже")

@router.message(F.text == 'Проанализировать🔍')
async def handler_button_analyze(message: types.Message):
    try:
        user = message.from_user.id
        image_path = get_last_user_path(user)

        await add_action(user, 'analysis face', action_info=None)
        await message.answer("Анализирую...⏳")

        info = analyze_face_photo(image_path)

        if not info:
            await message.answer("Я не смог проанализировать данного человека")
        await message.answer(f"Вы {info[0]} и ваш возраст {info[3]}")
        await message.answer(f"Я думаю ваша раса - {info[1]}, \nи ваша эмоция - {info[2]}")

        await AsyncORM.add_action(
            message.from_user.id,
            'result analysis face',
            f"gender:{info[0]}, race:{info[1]}, emotion:{info[2]}, age:{info[3]}"
        )
        await message.answer("Можете отправить еще что-нибудь")
    except Exception as e:
        await add_action(message.from_user.id, 'analysis button', action_info=f'{e}')
        await message.answer("Упс... Что-то пошло не так, попробуйте позже")
