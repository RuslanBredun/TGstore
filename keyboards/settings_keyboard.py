from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from typing import Optional
from languages.languages import languages

from db.sql import DataBase
db = DataBase('my_database.db')


class SettingsCallbackFactory(CallbackData, prefix="settings"):
    type: str
    currency: Optional[str] = None
    lang: Optional[str] = None


async def get_settings_keyboard(user_id):
    keyboard = InlineKeyboardBuilder()
    lang = await db.get_lang(user_id)
    lang = lang[0][0]

    keyboard.row(
        InlineKeyboardButton(text=languages[lang]['change_currency'],
                             callback_data=SettingsCallbackFactory(type="currency").pack()),
        InlineKeyboardButton(text=languages[lang]['change_language'],
                             callback_data=SettingsCallbackFactory(type="language").pack()))

    keyboard.row(InlineKeyboardButton(text=languages[lang]['back'],
                                      callback_data=SettingsCallbackFactory(type="back").pack()))

    return keyboard


async def get_currency_keyboard(user_id):
    keyboard = InlineKeyboardBuilder()

    currency = await db.get_currency(user_id)
    currency = currency[0][0]
    lang = await db.get_lang(user_id)
    lang = lang[0][0]

    keyboard.row(
        InlineKeyboardButton(text=f"{'✅ USD $' if currency=='usd' else 'USD $'}",
                             callback_data=SettingsCallbackFactory(type="set_currency",
                                                                   currency="usd").pack()),
        InlineKeyboardButton(text=f"{'✅ EUR €' if currency=='eur' else 'EUR €'}",
                             callback_data=SettingsCallbackFactory(type="set_currency",
                                                                   currency="eur").pack()),
        InlineKeyboardButton(text=f"{'✅ RON L' if currency=='ron' else 'RON L'}",
                             callback_data=SettingsCallbackFactory(type="set_currency",
                                                                   currency="ron").pack()),
        InlineKeyboardButton(text=f"{'✅ PLN zł' if currency=='pln' else 'PLN zł'}",
                             callback_data=SettingsCallbackFactory(type="set_currency",
                                                                   currency="pln").pack()))

    keyboard.row(InlineKeyboardButton(text=languages[lang]['back'],
                                      callback_data=SettingsCallbackFactory(type="back_settings").pack()),
                 InlineKeyboardButton(text=languages[lang]['main_menu'],
                                      callback_data=SettingsCallbackFactory(type="back").pack())
                 )

    return keyboard


async def get_set_lang_keyboard(user_id):
    keyboard = InlineKeyboardBuilder()

    lang = await db.get_lang(user_id)
    lang = lang[0][0]

    keyboard.row(
        InlineKeyboardButton(text=f"{'✅ ru' if lang=='ru' else 'ru'}",
                             callback_data=SettingsCallbackFactory(type="set_lang",
                                                                   lang="ru").pack()),
        InlineKeyboardButton(text=f"{'✅ pl' if lang=='pl' else 'pl'}",
                             callback_data=SettingsCallbackFactory(type="set_lang",
                                                                   lang="pl").pack()),
        InlineKeyboardButton(text=f"{'✅ uk' if lang=='uk' else 'uk'}",
                             callback_data=SettingsCallbackFactory(type="set_lang",
                                                                   lang="uk").pack()),
        InlineKeyboardButton(text=f"{'✅ en' if lang=='en' else 'en'}",
                             callback_data=SettingsCallbackFactory(type="set_lang",
                                                                   lang="en").pack()),
        InlineKeyboardButton(text=f"{'✅ bg' if lang=='bg' else 'bg'}",
                             callback_data=SettingsCallbackFactory(type="set_lang",
                                                                   lang="bg").pack()),
        InlineKeyboardButton(text=f"{'✅ ro' if lang=='ro' else 'ro'}",
                             callback_data=SettingsCallbackFactory(type="set_lang",
                                                                   lang="ro").pack()),
        InlineKeyboardButton(text=f"{'✅ el' if lang=='el' else 'el'}",
                             callback_data=SettingsCallbackFactory(type="set_lang",
                                                                   lang="el").pack()),
        InlineKeyboardButton(text=f"{'✅ de' if lang=='de' else 'de'}",
                             callback_data=SettingsCallbackFactory(type="set_lang",
                                                                   lang="de").pack()),
        width=4)

    keyboard.row(InlineKeyboardButton(text=languages[lang]['back'],
                                      callback_data=SettingsCallbackFactory(type="back_settings").pack()),
                 InlineKeyboardButton(text=languages[lang]['main_menu'],
                                      callback_data=SettingsCallbackFactory(type="back").pack())
                 )

    return keyboard


async def get_init_lang_keyboard(user_id):
    keyboard = InlineKeyboardBuilder()

    lang = await db.get_lang(user_id)
    lang = lang[0][0]

    keyboard.row(
        InlineKeyboardButton(text=f"{'✅ ru' if lang == 'ru' else 'ru'}",
                             callback_data=SettingsCallbackFactory(type="set_init_lang",
                                                                   lang="ru").pack()),
        InlineKeyboardButton(text=f"{'✅ pl' if lang == 'pl' else 'pl'}",
                             callback_data=SettingsCallbackFactory(type="set_init_lang",
                                                                   lang="pl").pack()),
        InlineKeyboardButton(text=f"{'✅ uk' if lang == 'uk' else 'uk'}",
                             callback_data=SettingsCallbackFactory(type="set_init_lang",
                                                                   lang="uk").pack()),
        InlineKeyboardButton(text=f"{'✅ en' if lang == 'en' else 'en'}",
                             callback_data=SettingsCallbackFactory(type="set_init_lang",
                                                                   lang="en").pack()),
        InlineKeyboardButton(text=f"{'✅ bg' if lang == 'bg' else 'bg'}",
                             callback_data=SettingsCallbackFactory(type="set_init_lang",
                                                                   lang="bg").pack()),
        InlineKeyboardButton(text=f"{'✅ ro' if lang == 'ro' else 'ro'}",
                             callback_data=SettingsCallbackFactory(type="set_init_lang",
                                                                   lang="ro").pack()),
        InlineKeyboardButton(text=f"{'✅ el' if lang == 'el' else 'el'}",
                             callback_data=SettingsCallbackFactory(type="set_init_lang",
                                                                   lang="el").pack()),
        InlineKeyboardButton(text=f"{'✅ de' if lang == 'de' else 'de'}",
                             callback_data=SettingsCallbackFactory(type="set_init_lang",
                                                                   lang="de").pack()),
        width=4)

    keyboard.adjust(4)

    return keyboard
