from aiogram import Bot
from aiogram.types import BotCommand

async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/start',
                   description='Старт бота'),
    ]

    await bot.set_my_commands(main_menu_commands)