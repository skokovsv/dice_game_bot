


import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
import config

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = config.TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text='map')],
        [types.KeyboardButton(text='/cube')]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите команду'
    )
    await message.answer("Hello!",reply_markup=keyboard)


@dp.message(Command("cube"))
async def cmd_dice(message: types.Message):
    msg = await message.answer_dice(emoji="🎲")
    print(msg.dice.value)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())