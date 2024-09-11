from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from db.sql import DataBase
from languages.languages import languages, ImagePath
from currency_converter import CurrencyConverter
converter = CurrencyConverter()


db = DataBase('my_database.db')


class CartCallbackFactory(CallbackData, prefix="cart"):
    type: str
    product_id: Optional[int] = None
    category_id: Optional[int] = None
    page_num: Optional[int] = None


async def get_cart_keyboard(page, user_id):

    keyboard = InlineKeyboardBuilder()

    data = await db.get_cart(user_id)
    lang = await db.get_lang(user_id)
    lang = lang[0][0]

    currency = await db.get_currency(user_id)
    currency = currency[0][0]

    price = 0
    for i in data:
        price += i[2] * round(converter.convert(i[4], 'USD', currency.upper()), 2)

    max_page = len(data)-1
    page = min(page, max_page)

    info = None

    if data:
        info = data[page][5], data[page][6]
        keyboard.button(text=f'{data[page][2]} x {data[page][0]}',
                        callback_data=CartCallbackFactory(type="cart"))
        keyboard.row(InlineKeyboardButton(text='🔽',
                                          callback_data=CartCallbackFactory(type="minus",
                                                                            product_id=f"{data[page][3]}",
                                                                            category_id=f"{data[page][1]}",
                                                                            page_num=page).pack()),
                     InlineKeyboardButton(text='🔼',
                                          callback_data=CartCallbackFactory(type="plus",
                                                                            product_id=f"{data[page][3]}",
                                                                            category_id=f"{data[page][1]}",
                                                                            page_num=page).pack()),
                     InlineKeyboardButton(text='❌',
                                          callback_data=CartCallbackFactory(type="del",
                                                                            product_id=f"{data[page][3]}",
                                                                            category_id=f"{data[page][1]}",
                                                                            page_num=page).pack()))
        keyboard.row(InlineKeyboardButton(text='<<',
                                          callback_data=CartCallbackFactory(
                                              type="nav",
                                              page_num=0).pack()),
                     InlineKeyboardButton(text='<',
                                          callback_data=CartCallbackFactory(
                                              type="nav",
                                              page_num=min(max(page-1, 0), max_page)).pack()),
                     InlineKeyboardButton(text=f'{page+1}/{max_page+1}',
                                          callback_data=CartCallbackFactory(
                                              type="mid").pack()),
                     InlineKeyboardButton(text='>',
                                          callback_data=CartCallbackFactory(
                                              type="nav",
                                              page_num=min(max(page + 1, 0), max_page)).pack()),
                     InlineKeyboardButton(text='>>',
                                          callback_data=CartCallbackFactory(
                                              type="nav",
                                              page_num=max_page).pack()))

    keyboard.row(InlineKeyboardButton(text=f'{languages[lang]["checkout"]}: {round(price, 2)} {currency.upper()}',
                                      callback_data=CartCallbackFactory(
                                          type="buy").pack()))
    keyboard.row(InlineKeyboardButton(text=languages[lang]["back"],
                                      callback_data=CartCallbackFactory(
                                          type="back").pack()))
    if not info:
        info = (languages[lang]["empty_cart"],
                f"{ImagePath}empty.png")
    return keyboard, info
