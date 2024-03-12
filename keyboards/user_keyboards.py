from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU

# ------- Создаем клавиатуру через start_kb -------

# Создаем кнопки стартового меню
button_info_goods = KeyboardButton(text=LEXICON_RU['info_goods'])
button_stop_mailing = KeyboardButton(text=LEXICON_RU['stop_mailing'])
button_get_active_subs = KeyboardButton(text=LEXICON_RU['get_active_subs'])
button_get_info_from_db = KeyboardButton(text=LEXICON_RU['get_info_from_db'])

# Инициализируем билдер для стартовой клавиатуры
start_kb_builder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер
start_kb_builder.row(button_info_goods, button_get_active_subs,
                     button_stop_mailing, button_get_info_from_db, width=1)

# Создаем стартовую клавиатуру
start_kb: ReplyKeyboardMarkup = start_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True,
    input_field_placeholder=LEXICON_RU['start_placeholder']
)

# ------- Создаем клавиатуру через subscribe_kb -------

# Создаем объекты инлайн-кнопки
subscribe_button = InlineKeyboardButton(
    text=LEXICON_RU['subscribe'],
    callback_data='subscribe'
)

get_another_button = InlineKeyboardButton(
    text=LEXICON_RU['get_another'],
    callback_data='get_another'
)

# Создаем объект инлайн-клавиатуры
subscribe_kb = InlineKeyboardMarkup(
    inline_keyboard=[[subscribe_button], [get_another_button]]
)

