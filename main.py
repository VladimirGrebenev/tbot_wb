import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers
from services.mailing_subscriptions import mailing_subscriptions
from keyboards.set_menu import set_main_menu


# Функция конфигурирования и запуска бота
async def main():
    # Загружаем конфиг в переменную config
    config: Config = load_config('./config_data/.env')

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    # Инициализируем крон
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(mailing_subscriptions, trigger='interval',
                      seconds=10,
                      kwargs={'bot': bot})
    scheduler.start()

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Регистрируем асинхронную функцию для меню в диспетчере,
    # которая будет выполняться на старте бота,
    dp.startup.register(set_main_menu)

    # Пропускаем накопившиеся апдейты и запускаем поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# Запускаем бот
if __name__ == '__main__':
    asyncio.run(main())
