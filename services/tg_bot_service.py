from aiogram import Dispatcher, Bot, types, executor
from aiogram.dispatcher.filters import CommandStart, Command
from environs import Env

import output as s_out
import logger as lg
import services.service as srv
from exceptions import *

env = Env()
env.read_env()
BOT_TOKEN = env.str("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer(text=s_out.WELCOME)
    await dp.bot.set_my_commands(
        [
            types.BotCommand("complex_signs", "Допустимые знаки с комплексными числами"),
            types.BotCommand("rational_signs", "Допустимые знаки с рациональными числами"),
            types.BotCommand("help", "Информация о калькуляторе"),
        ]
    )


@dp.message_handler(Command("complex_signs"))
async def complex_signs(message: types.Message):
    await message.answer(text=s_out.COMPLEX_OPER)


@dp.message_handler(Command("rational_signs"))
async def rational_signs(message: types.Message):
    await message.answer(text=s_out.RAT_OPER)


@dp.message_handler(Command("help"))
async def helper(message: types.Message):
    await message.answer(text=s_out.INFO)


@dp.message_handler()
async def solve_expression(message: types.Message):
    try:
        line = message.text
        lg.log(lg.INPUT, message.text)
        line.strip()
        result = srv.get_result(line)
        lg.log(lg.ANSWER, result)
        await message.answer(s_out.RESULT + result)
    except InputError as error:
        lg.log(lg.EXCEPTION, str(error))
        await message.answer(str(error) + " " + s_out.TRY_AGAN)
    except AnswerTimeError as error:
        lg.log(lg.ERROR, str(error))
        await message.answer(s_out.TOTAL_ERROR + " " + str(error))
    except Exception as error:
        lg.log(lg.ERROR, str(error))
        await message.answer(s_out.TOTAL_ERROR)


def launch():
    executor.start_polling(dispatcher=dp, skip_updates=True)
