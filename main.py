


import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest
from aiogram import F
import config

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = config.TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

count = 5  # количество попыток

@dp.message(Command("clear"))
async def cmd_clear(message: types.Message, bot: Bot) -> None:
    try:
        # Все сообщения, начиная с текущего и до первого (message_id = 0)
        for i in range(message.message_id, 0, -1):
            await bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest as ex:
        # Если сообщение не найдено (уже удалено или не существует),
        # код ошибки будет "Bad Request: message to delete not found"
        if ex.message == "Bad Request: message to delete not found":
            print("Все сообщения удалены")

def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="1", callback_data="st_1"),
            types.InlineKeyboardButton(text="2", callback_data="st_2"),
            types.InlineKeyboardButton(text="3", callback_data="st_3"),
            types.InlineKeyboardButton(text="4", callback_data="st_4"),
            types.InlineKeyboardButton(text="5", callback_data="st_5"),
            types.InlineKeyboardButton(text="6", callback_data="st_6")
        ]

    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_repeat_game():
    buttons = [
        [
            types.InlineKeyboardButton(text="yes", callback_data="yes"),
            types.InlineKeyboardButton(text="no", callback_data="no"),

        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_start_bot():
    kb = [
        [types.KeyboardButton(text='map')],
        [types.KeyboardButton(text='/cube')]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите команду'
    )
    return keyboard



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

    global count
    count = 5
    await message.answer(f'На что ставим?',reply_markup=get_keyboard())
    #msg = await message.answer_dice(emoji="🎲")
    #print(msg.dice.value)

@dp.callback_query(F.data.startswith("st_"))
async def make_stavka(callback: types.CallbackQuery):
    val = callback.data.split("_")[1]


    msg = await callback.message.answer_dice(emoji="🎲")
    print(msg.dice.value)
    print(type(val))
    print(type(msg.dice.value))
    global count

    if count>1:

        if int(val) == msg.dice.value:
            await callback.message.answer(f'You win!!!  {count}k y сергея')
            await callback.message.answer_sticker("CAACAgIAAxkBAAEL8tNmIX1ZNFna7JfFTQw83Paz8XWGKgACSBAAAuSWWEk1O9YRMsMYpTQE")

        else:
            count-=1
            await callback.message.answer(f'не повезло(((\nосталось попыток {count}',reply_markup=get_keyboard())
            # await callback.message.answer('((( сыграем ещё?', reply_markup=get_repeat_game())
    else:
        await callback.message.answer('you lose!!!\nвы должны 5к сергею!',reply_markup=get_start_bot())


@dp.callback_query(F.data == 'yes')
async def repeat_stavka(callback: types.CallbackQuery):
    await callback.message.answer('На что ставим?',reply_markup=get_keyboard())


@dp.callback_query(F.data == 'no')
async def end_game(callback: types.CallbackQuery):
    await callback.message.answer('ok bye', reply_markup=get_start_bot())



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())