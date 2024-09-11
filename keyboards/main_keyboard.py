from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from db.sql import DataBase
from languages.languages import languages

db = DataBase('my_database.db')


class MainMenuCallbackFactory(CallbackData, prefix="main"):
    type: str


async def get_main_keyboard(user_id):
    builder = InlineKeyboardBuilder()

    lang = await db.get_lang(user_id)
    lang = lang[0][0]

    builder.row(
        InlineKeyboardButton(text=languages[lang]['catalog'],
                             callback_data=MainMenuCallbackFactory(type="catalog").pack()),
        InlineKeyboardButton(text=languages[lang]['cart'],
                             callback_data=MainMenuCallbackFactory(type="cart").pack()),
        InlineKeyboardButton(text=languages[lang]['favorites'],
                             callback_data=MainMenuCallbackFactory(type="favorites").pack()),
        InlineKeyboardButton(text=languages[lang]['promotions'],
                             callback_data=MainMenuCallbackFactory(type="promotion").pack()),
        InlineKeyboardButton(text=languages[lang]['settings'],
                             callback_data=MainMenuCallbackFactory(type="settings").pack()),
        InlineKeyboardButton(text=languages[lang]['ai_consultant'],
                             callback_data=MainMenuCallbackFactory(type="ai").pack()))

    builder.adjust(2)

    return builder

