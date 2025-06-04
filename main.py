import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from config import BOT_TOKEN
from database import init_db, add_user, add_tracking, get_all_tracking, update_price
from parser import get_price

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
init_db()

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Добавить артикул")],
        [KeyboardButton(text="📋 Мои товары")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: types.Message):
    add_user(message.from_user.id)
    await message.answer(
        "Привет! Я бот для отслеживания цен на Wildberries.\n\n"
        "Отправь мне артикул товара, и я начну отслеживать цену!",
        reply_markup=main_kb
    )

@dp.message(lambda message: message.text == "➕ Добавить артикул")
async def ask_article(message: types.Message):
    await message.answer("Отправь артикул товара:")

@dp.message()
async def handle_article(message: types.Message):
    if message.text.isdigit():
        article = message.text
        price = get_price(article)
        if price:
            add_tracking(message.from_user.id, article, price)
            await message.answer(f"✅ Добавлен товар {article}. Текущая цена: {price}₽.")
        else:
            await message.answer("❌ Не удалось получить цену. Проверь артикул.")
    else:
        await message.answer("Пожалуйста, отправь только номер артикула.")

async def price_checker():
    while True:
        tracking_data = get_all_tracking()
        for user_id, article, old_price, levels in tracking_data:
            new_price = get_price(article)
            if new_price and new_price < old_price:
                percent_drop = 100 * (old_price - new_price) / old_price
                notify_thresholds = [int(p) for p in levels.split(",")]
                for threshold in notify_thresholds:
                    if percent_drop >= threshold:
                        await bot.send_message(
                            user_id,
                            f"📉 Цена на товар {article} упала на {int(percent_drop)}%!\n"
                            f"Старая: {old_price}₽\nНовая: {new_price}₽"
                        )
                        update_price(user_id, article, new_price)
                        break
        await asyncio.sleep(3600)

async def main():
    asyncio.create_task(price_checker())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
