import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "8577118492:AAGL6cjqcXSCvChlGyQPtAVNmX8nVFb6JLc"
ADMIN_ID = 5203710686

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Order(StatesGroup):
    description = State()
    budget = State()
    code_description = State()
    code_budget = State()
    bot_description = State()
    bot_budget = State()
    mini_description = State()
    mini_budget = State()

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Услуги", callback_data="services")],
        [InlineKeyboardButton(text="Отзывы", callback_data="reviews")],
    ])

def services_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Написание приложения", callback_data="app")],
        [InlineKeyboardButton(text="Написание кода", callback_data="code")],
        [InlineKeyboardButton(text="Написание Telegram Бота", callback_data="tgbot")],
        [InlineKeyboardButton(text="Написание Mini App", callback_data="miniapp")],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ])

def platform_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Android", callback_data="android")],
        [InlineKeyboardButton(text="iOS", callback_data="ios")],
        [InlineKeyboardButton(text="Назад", callback_data="services")],
    ])

def languages_menu():
    langs = ["Python", "JavaScript", "TypeScript", "Go", "Rust", "C++", "C#", "Java", "Kotlin", "Swift", "PHP", "Ruby"]
    buttons = [[InlineKeyboardButton(text=lang, callback_data="lang_" + lang)] for lang in langs]
    buttons.append([InlineKeyboardButton(text="Назад", callback_data="services")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Здравствуйте! Добро пожаловать в сервис mogged.\n\nЯ помогу вам оформить заявку на нужную услугу.",
        reply_markup=main_menu()
    )

@dp.callback_query(F.data == "back")
async def back_to_main(call: CallbackQuery):
    await call.message.edit_text(
        "Здравствуйте! Добро пожаловать в сервис mogged.\n\nЯ помогу вам оформить заявку на нужную услугу.",
        reply_markup=main_menu()
    )

@dp.callback_query(F.data == "reviews")
async def reviews(call: CallbackQuery):
    await call.message.edit_text(
        "Извините, отзывы пока недоступны из-за удаления чата.\n\nВы можете посмотреть мои отзывы на FunPay: alex11911",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back")]
        ])
    )

@dp.callback_query(F.data == "services")
async def services(call: CallbackQuery):
    await call.message.edit_text("Выберите услугу:", reply_markup=services_menu())

@dp.callback_query(F.data == "app")
async def app_service(call: CallbackQuery):
    await call.message.edit_text("Выберите платформу:", reply_markup=platform_menu())

@dp.callback_query(F.data.in_({"android", "ios"}))
async def app_platform(call: CallbackQuery, state: FSMContext):
    platform = "Android" if call.data == "android" else "iOS"
    await state.update_data(service="Приложение", platform=platform)
    await state.set_state(Order.description)
    await call.message.edit_text("Платформа: " + platform + "\n\nВведите, что вы хотите видеть в приложении:")

@dp.message(Order.description)
async def app_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Order.budget)
    await message.answer("Какой ваш бюджет?")

@dp.message(Order.budget)
async def app_budget(message: Message, state: FSMContext):
    await state.update_data(budget=message.text)
    await send_order(message, state)

@dp.callback_query(F.data == "code")
async def code_service(call: CallbackQuery, state: FSMContext):
    await state.update_data(service="Написание кода")
    await call.message.edit_text("Выберите язык программирования:", reply_markup=languages_menu())

@dp.callback_query(F.data.startswith("lang_"))
async def code_language(call: CallbackQuery, state: FSMContext):
    lang = call.data.replace("lang_", "")
    await state.update_data(language=lang)
    await state.set_state(Order.code_description)
    await call.message.edit_text("Язык: " + lang + "\n\nОпишите ваше техническое задание:")

@dp.message(Order.code_description)
async def code_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Order.code_budget)
    await message.answer("Какой ваш бюджет?")

@dp.message(Order.code_budget)
async def code_budget(message: Message, state: FSMContext):
    await state.update_data(budget=message.text)
    await send_order(message, state)

@dp.callback_query(F.data == "tgbot")
async def tgbot_service(call: CallbackQuery, state: FSMContext):
    await state.update_data(service="Telegram Bot")
    await state.set_state(Order.bot_description)
    await call.message.edit_text("Опишите, что вы хотите видеть в боте:")

@dp.message(Order.bot_description)
async def bot_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Order.bot_budget)
    await message.answer("Какой ваш бюджет?")

@dp.message(Order.bot_budget)
async def bot_budget(message: Message, state: FSMContext):
    await state.update_data(budget=message.text)
    await send_order(message, state)

@dp.callback_query(F.data == "miniapp")
async def miniapp_service(call: CallbackQuery, state: FSMContext):
    await state.update_data(service="Mini App")
    await state.set_state(Order.mini_description)
    await call.message.edit_text("Опишите, что вы хотите видеть в Mini App:")

@dp.message(Order.mini_description)
async def mini_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Order.mini_budget)
    await message.answer("Какой ваш бюджет?")

@dp.message(Order.mini_budget)
async def mini_budget(message: Message, state: FSMContext):
    await state.update_data(budget=message.text)
    await send_order(message, state)

async def send_order(message: Message, state: FSMContext):
    data = await state.get_data()
    user = message.from_user

    username = "@" + user.username if user.username else "нет"

    text = "Новая заявка!\n\n"
    text += "Имя: " + user.full_name + "\n"
    text += "ID: " + str(user.id) + "\n"
    text += "Username: " + username + "\n\n"
    text += "Услуга: " + data.get("service", "-") + "\n"

    if data.get("platform"):
        text += "Платформа: " + data["platform"] + "\n"
    if data.get("language"):
        text += "Язык: " + data["language"] + "\n"

    text += "ТЗ: " + data.get("description", "-") + "\n"
    text += "Бюджет: " + message.text + "\n"

    await bot.send_message(ADMIN_ID, text)
    await state.clear()
    await message.answer("Ваша заявка отправлена! Скоро с вами свяжутся.", reply_markup=main_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())