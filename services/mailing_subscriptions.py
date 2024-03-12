from aiogram import Bot
from models.methods import get_active_subscriptions
from lexicon.lexicon_ru import LEXICON_RU
from services.services import get_info_from_wb

async def mailing_subscriptions(bot: Bot):
    active_subs = get_active_subscriptions()
    for sub in active_subs:
        await bot.send_message(sub.user_id, text=LEXICON_RU['your_active_subs'])
        p_data = get_info_from_wb(sub.product_id)
        info = (f'Товар: {p_data["name"]}\n'
                f'Бренд: {p_data["brand"]}\n'
                f'Цена: {p_data["priceU"]} ₽\n'
                f'Распродажа: {p_data["salePriceU"]} ₽\n'
                f'Кол-во: {p_data["stock"]} шт.\n'
                f'id: {p_data["id"]}\n')
        await bot.send_message(sub.user_id, text=info)
