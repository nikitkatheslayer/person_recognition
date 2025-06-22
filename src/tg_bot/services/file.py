import os
from dotenv import load_dotenv
from tg_bot.services.state_user import set_user_path

load_dotenv()

async def save_file(bot, user, file_id, type_dir):
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name, file_ext = os.path.splitext(file_path)
    save_path = f"{os.getenv('PROJECT_ROOT')}/storage/{type_dir}/{file_id}{file_ext}"

    set_user_path(user, save_path)

    downloaded = await bot.download_file(file_path)
    with open(save_path, "wb") as new_file:
        new_file.write(downloaded.read())

    return save_path, file_name, file_ext

def get_file(type_dir, file_id, file_ext, **kwargs):
    is_source = kwargs.get("is_source")
    match is_source:
        case True:
            file_path = f"{os.getenv('PROJECT_ROOT')}/storage/{type_dir}/{file_id}{file_ext}"
        case _:
            file_path = f"{os.getenv('PROJECT_ROOT')}/storage/{type_dir}/{file_id}_detected{file_ext}"
    return file_path