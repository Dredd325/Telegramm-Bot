import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = “8577118492:AAGL6cjqcXSCvChlGyQPtAVNmX8nVFb6JLc”
ADMIN_ID = 5203710686  # Ваш Telegram ID

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Order(StatesGroup):
platform = State()
description = State()
budget = State()
language = State()
code_description = State()
code_budget = State()
bot_description = State()
bot_budget = State()
mini_description = State()
mini_budget = State()

def main_menu():
return InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(text=“🛠 Услуги”, callback_data=“services”)],
[InlineKeyboardButton(text=“⭐️ Отзывы”, callback_data=“reviews”)],
])

def services_menu():
return InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(text=“📱 Написание приложения”, callback_data=“app”)],
[InlineKeyboardButton(text=“💻 Написание кода”, callback_data=“code”)],
[InlineKeyboardButton(text=“🤖 Написание Telegram Бота”, callback_data=“tgbot”)],
[InlineKeyboardButton(text=“🧩 Написание Mini App”, callback_data=“miniapp”)],
[InlineKeyboardButton(text=“◀️ Назад”, callback_data=“back”)],
])

def platform_menu():
return InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(text=“🤖 Android”, callback_data=“android”)],
[InlineKeyboardButton(text=“🍎 iOS”, callback_data=“ios”)],
[InlineKeyboardButton(text=“◀️ Назад”, callback_data=“services”)],
])

def languages_menu():
langs = [“Python”, “JavaScript”, “TypeScript”, “Go”, “Rust”, “C++”, “C#”, “Java”, “Kotlin”, “Swift”, “PHP”, “Ruby”]
buttons = [[InlineKeyboardButton(text=lang, callback_data=f”lang_{lang}”)] for lang in langs]
buttons.append([InlineKeyboardButton(text=“◀️ Назад”, callback_data=“services”)])
return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(CommandStart())
async def start(message: Message):
await message.answer(
“👋 Здравствуйте! Добро пожаловать в сервис **mogged**.\n\nЯ помогу вам оформить заявку на нужную услугу.”,
parse_mode=“Markdown”,
reply_markup=main_menu()
)

@dp.callback_query(F.data == “back”)
async def back_to_main(call: CallbackQuery):
await call.message.edit_text(
“👋 Здравствуйте! Добро пожаловать в сервис **mogged**.\n\nЯ помогу вам оформить заявку на нужную услугу.”,
parse_mode=“Markdown”,
reply_markup=main_menu()
)

@dp.callback_query(F.data == “reviews”)
async def reviews(call: CallbackQuery):
await call.message.edit_text(
“😔 Извините, отзывы пока недоступны из-за удаления чата.\n\n”
“Вы можете посмотреть мои отзывы на FunPay: **alex11911**”,
parse_mode=“Markdown”,
reply_markup=InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(text=“◀️ Назад”, callback_data=“back”)]
])
)

@dp.callback_query(F.data == “services”)
async def services(call: CallbackQuery):
await call.message.edit_text(“🛠 Выберите услугу:”, reply_markup=services_menu())

@dp.callback_query(F.data == “app”)
async def app_service(call: CallbackQuery):
await call.message.edit_text(“📱 Выберите платформу:”, reply_markup=platform_menu())

@dp.callback_query(F.data.in_({“android”, “ios”}))
async def app_platform(call: CallbackQuery, state: FSMContext):
platform = “Android” if call.data == “android” else “iOS”
await state.update_data(service=“Приложение”, platform=platform)
await state.set_state(Order.description)
await call.message.edit_text(f”✅ Платформа: **{platform}**\n\n📝 Введите, что вы хотите видеть в приложении:”, parse_mode=“Markdown”)

@dp.message(Order.description)
async def app_description(message: Message, state: FSMContext):
await state.update_data(description=message.text)
await state.set_state(Order.budget)
await message.answer(“💰 Какой ваш бюджет?”)

@dp.message(Order.budget)
async def app_budget(message: Message, state: FSMContext):
await state.update_data(budget=message.text)
await send_order(message, state)

@dp.callback_query(F.data == “code”)
async def code_service(call: CallbackQuery, state: FSMContext):
await state.update_data(service=“Написание кода”)
await call.message.edit_text(“💻 Выберите язык программирования:”, reply_markup=languages_menu())

@dp.callback_query(F.data.startswith(“lang_”))
async def code_language(call: CallbackQuery, state: FSMContext):
lang = call.data.replace(“lang_”, “”)
await state.update_data(language=lang)
await state.set_state(Order.code_description)
await call.message.edit_text(f”✅ Язык: **{lang}**\n\n📝 Опишите ваше техническое задание:”, parse_mode=“Markdown”)

@dp.message(Order.code_description)
async def code_description(message: Message, state: FSMContext):
await state.update_data(description=message.text)
await state.set_state(Order.code_budget)
await message.answer(“💰 Какой ваш бюджет?”)

@dp.message(Order.code_budget)
async def code_budget(message: Message, state: FSMContext):
await state.update_data(budget=message.text)
await send_order(message, state)

@dp.callback_query(F.data == “tgbot”)
async def tgbot_service(call: CallbackQuery, state: FSMContext):
await state.update_data(service=“Telegram Бот”)
await state.set_state(Order.bot_description)
await call.message.edit_text(“🤖 Опишите, что вы хотите видеть в боте:”)

@dp.message(Order.bot_description)
async def bot_description(message: Message, state: FSMContext):
await state.update_data(description=message.text)
await state.set_state(Order.bot_budget)
await message.answer(“💰 Какой ваш бюджет?”)

@dp.message(Order.bot_budget)
async def bot_budget(message: Message, state: FSMContext):
await state.update_data(budget=message.text)
await send_order(message, state)

@dp.callback_query(F.data == “miniapp”)
async def miniapp_service(call: CallbackQuery, state: FSMContext):
await state.update_data(service=“Mini App”)
await state.set_state(Order.mini_description)
await call.message.edit_text(“🧩 Опишите, что вы хотите видеть в Mini App:”)

@dp.message(Order.mini_description)
async def mini_description(message: Message, state: FSMContext):
await state.update_data(description=message.text)
await state.set_state(Order.mini_budget)
await message.answer(“💰 Какой ваш бюджет?”)

@dp.message(Order.mini_budget)
async def mini_budget(message: Message, state: FSMContext):
await state.update_data(budget=message.text)
await send_order(message, state)

async def send_order(message: Message, state: FSMContext):
data = await state.get_data()
user = message.from_user

```
text = (
    f"📬 *Новая заявка!*\n\n"
    f"👤 Имя: {user.full_name}\n"
    f"🆔 ID: `{user.id}`\n"
    f"📛 Username: @{user.username if user.username else 'нет'}\n\n"
    f"🛠 Услуга: {data.get('service', '—')}\n"
)

if data.get("platform"):
    text += f"📱 Платформа: {data['platform']}\n"
if data.get("language"):
    text += f"💻 Язык: {data['language']}\n"

text += (
    f"📝 ТЗ: {data.get('description', '—')}\n"
    f"💰 Бюджет: {data.get('budget', message.text)}\n"
)

await bot.send_message(ADMIN_ID, text, parse_mode="Markdown")
await state.clear()
await message.answer(
    "✅ Ваша заявка отправлена! Скоро с вами свяжутся.",
    reply_markup=main_menu()
)
```

async def main():
await dp.start_polling(bot)

if **name** == “**main**”:
asyncio.run(main())