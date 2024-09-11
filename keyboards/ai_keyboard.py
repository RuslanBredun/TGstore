from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State

from languages.languages import languages

from db.sql import DataBase
db = DataBase('my_database.db')


class AIState(StatesGroup):
    ai = State()


class AICallbackFactory(CallbackData, prefix="ai"):
    type: str


async def get_ai_keyboard(user_id):
    keyboard = ReplyKeyboardBuilder()
    lang = await db.get_lang(user_id)
    lang = lang[0][0]

    keyboard.row(
        KeyboardButton(text=languages[lang]["tell_promo"]),
        KeyboardButton(text=languages[lang]["tell_products"])
    )

    keyboard.row(KeyboardButton(text=languages[lang]["back"]))

    return keyboard
