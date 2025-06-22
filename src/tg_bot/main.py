import asyncio
import os

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from tg_bot.handlers import commands, exceptions, contact, photo, video, buttons, callbacks
from tg_bot.services.check_user import CheckUserMiddleware

load_dotenv()

async def main():
    bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.message.middleware(CheckUserMiddleware())

    dp.include_routers(commands.router)
    dp.include_routers(callbacks.router)
    dp.include_routers(contact.router)
    dp.include_routers(photo.router)
    dp.include_routers(video.router)
    dp.include_routers(buttons.router)
    dp.include_routers(exceptions.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())