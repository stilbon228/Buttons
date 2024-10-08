from __future__ import annotations
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = '6716269950:AAFtw0N75Rz9Ce4l0Xk7k__fN7b77ZXu1iQ'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

LEXICON: dict[str, str] = {
    'but_1': 'Кнопка 1',
    'but_2': 'Кнопка 2',
    'but_3': 'Кнопка 3',
    'but_4': 'Кнопка 4',
    'but_5': 'Кнопка 5',
    'but_6': 'Кнопка 6',
    'but_7': 'Кнопка 7',
    'back_to_main': 'Вернуться в главное меню',
    'proverb': 'Написать пословицу',
    'message': 'Напечатать сообщение'
}

BUTTONS: dict[str, str] = {
    'btn_1': '1',
    'btn_2': '2',
    'btn_3': '3',
    'btn_4': '4',
    'btn_5': '5',
    'btn_6': '6',
    'btn_7': '7',
    'btn_8': '8',
    'btn_9': '9',
    'btn_10': '10',
    'btn_11': '11',
    'back_to_main': 'back_to_main',
    'proverb': 'proverb',
    'message': 'message'
}

# Преобразуем dict_keys в список один раз
MAIN_BUTTONS = list(BUTTONS.keys())[:5]

# Функция для генерации инлайн-клавиатур "на лету"
def create_inline_kb(width: int,
                     *args: str,
                     last_btn: str | None = None,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)
    # Добавляем в билдер последнюю кнопку, если она передана в функцию
    if last_btn:
        kb_builder.row(InlineKeyboardButton(
            text=last_btn,
            callback_data='last_btn'
        ))

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять в чат клавиатуру
@dp.message(CommandStart())
async def process_start_command(message: Message):
    keyboard = create_inline_kb(5, *MAIN_BUTTONS)
    await message.answer(
        text='Это инлайн-клавиатура, сформированная функцией <code>create_inline_kb</code>',
        reply_markup=keyboard
    )

# Хэндлер для обработки нажатий на кнопки
@dp.callback_query(lambda c: c.data in MAIN_BUTTONS)
async def process_button(callback_query: types.CallbackQuery):
    if callback_query.data == 'btn_1':
        keyboard = create_inline_kb(1, 'back_to_main', 'proverb', 'message')
        await bot.send_message(callback_query.from_user.id, 'Вы выбрали Кнопку 1', reply_markup=keyboard)
    elif callback_query.data == 'btn_2':
        keyboard = create_inline_kb(2, 'back_to_main', 'proverb', 'message')
        await bot.send_message(callback_query.from_user.id, 'Вы выбрали Кнопку 2', reply_markup=keyboard)
    elif callback_query.data == 'btn_3':
        keyboard = create_inline_kb(3, 'back_to_main', 'proverb', 'message')
        await bot.send_message(callback_query.from_user.id, 'Вы выбрали Кнопку 3', reply_markup=keyboard)
    elif callback_query.data == 'btn_4':
        keyboard = create_inline_kb(4, 'back_to_main', 'proverb', 'message')
        await bot.send_message(callback_query.from_user.id, 'Вы выбрали Кнопку 4', reply_markup=keyboard)
    elif callback_query.data == 'btn_5':
        keyboard = create_inline_kb(5, 'back_to_main', 'proverb', 'message')
        await bot.send_message(callback_query.from_user.id, 'Вы выбрали Кнопку 5', reply_markup=keyboard)

# Хэндлер для возврата в главное меню
@dp.callback_query(lambda c: c.data == 'back_to_main')
async def process_back_to_main(callback_query: types.CallbackQuery):
    keyboard = create_inline_kb(5, *MAIN_BUTTONS)
    await bot.send_message(callback_query.from_user.id, 'Вы вернулись в главное меню', reply_markup=keyboard)

# Хэндлер для написания пословицы
@dp.callback_query(lambda c: c.data == 'proverb')
async def process_proverb(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Вот пословица: "NE pei on monday."')

# Хэндлер для напечатания сообщения
@dp.callback_query(lambda c: c.data == 'message')
async def process_message(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'You message')

if __name__ == '__main__':
    dp.run_polling(bot)