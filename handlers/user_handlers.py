from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from keyboards.user_keyboards import start_kb, subscribe_kb
from lexicon.lexicon_ru import LEXICON_RU
from services.services import get_info_from_wb
from models.methods import (create_subscription, get_last_subscriptions,
                            check_existing_subscription)

router = Router()

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage = MemoryStorage()


class FSM_WB_Product(StatesGroup):
    product_id = State()  # Состояние ожидания ввода id product


# Хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=start_kb)


# Хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=start_kb)


# Хэндлер срабатывает кнопку "запрос по артикулу"
@router.message(F.text == LEXICON_RU['info_goods'], )
async def process_info_goods_answer(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['write_goods_id'],
                         remove_keyboard=True)
    # Устанавливаем состояние ожидания ввода id product
    await state.set_state(FSM_WB_Product.product_id)


# Хэндлер срабатывает на ввод цифр (артикула)
@router.message(StateFilter(FSM_WB_Product.product_id),
                F.text.isdigit())
async def process_get_info_from_wb_answer(message: Message, state: FSMContext):
    p_data = get_info_from_wb(message.text)

    if p_data == None:
        await message.answer(text=LEXICON_RU['wrong_id'])
    else:
        # Сохраняем введенный артикул в хранилище по ключу "product_id"
        await state.update_data(product_id=message.text)

        info = (f'Товар: {p_data["name"]}\n'
                f'Бренд: {p_data["brand"]}\n'
                f'Цена: {p_data["priceU"]} ₽\n'
                f'Распродажа: {p_data["salePriceU"]} ₽\n'
                f'Кол-во: {p_data["stock"]} шт.\n'
                f'id: {p_data["id"]}')
        await message.answer(text=info, reply_markup=subscribe_kb)


# Хэндлер срабатывает кнопку "Подписаться"
@router.callback_query(F.data == 'subscribe')
async def process_subscribe_btn_press(callback: CallbackQuery,
                                      state: FSMContext):
    data = await state.get_data()
    product_id = data.get('product_id')

    if check_existing_subscription(callback.from_user.id, product_id):
        await callback.message.answer(
            text=LEXICON_RU['already_subscribed'],
            reply_markup=start_kb
        )
        await state.clear()
    else:
        create_subscription(callback.from_user.id, product_id)

        await callback.message.answer(
            text=LEXICON_RU['subscribe_added'],
            reply_markup=start_kb
        )

        await state.clear()


# Хэндлер срабатывает кнопку "Получить ещё информацию"
@router.callback_query(F.data == 'get_another')
async def process_get_another_btn_press(callback: CallbackQuery):
    await callback.message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=start_kb
    )


# Хэндлер срабатывает на кнопки "отказ рассылки"
@router.message(F.text == LEXICON_RU['stop_mailing'])
async def process_stop_mailing_answer(message: Message):
    await message.answer(text=LEXICON_RU['write_goods_id'])


# Хэндлер срабатывает на кнопку "инфа из базы данных"
@router.message(F.text == LEXICON_RU['get_info_from_db'])
async def process_get_info_from_db_answer(message: Message):
    last_s = get_last_subscriptions(message.from_user.id)
    await message.answer(text=LEXICON_RU['last_subscriptions'])
    for l in last_s:
        p_data = get_info_from_wb(l.product_id)
        info = (f'Товар: {p_data["name"]}\n'
                f'Бренд: {p_data["brand"]}\n'
                f'Цена: {p_data["priceU"]} ₽\n'
                f'Распродажа: {p_data["salePriceU"]} ₽\n'
                f'Кол-во: {p_data["stock"]} шт.\n'
                f'id: {p_data["id"]}\n')
        await message.answer(text=info)
