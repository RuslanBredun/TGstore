from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from db.sql import DataBase
from languages.languages import languages
from currency_converter import CurrencyConverter
converter = CurrencyConverter()

db = DataBase('my_database.db')


class ProductCallbackFactory(CallbackData, prefix="product"):
    type: str
    product_id: Optional[int] = None
    category_id: Optional[int] = None
    page_num: Optional[int] = None


async def gen_products_keyboard(category_id, user_id, page):

    keyboard = InlineKeyboardBuilder()

    data = await db.get_products(category_id)
    max_page = len(data)-1
    page = min(page, max_page)

    in_cart = await db.get_count_in_cart(user_id, data[page][1])
    in_fav = await db.get_in_fav(user_id, data[page][1])
    lang = await db.get_lang(user_id)
    lang = lang[0][0]

    info = data[page][4], data[page][5]

    currency = await db.get_currency(user_id)
    currency = currency[0][0]
    price = round(converter.convert(data[page][3], 'USD', currency.upper()), 2)

    keyboard.row(InlineKeyboardButton(text=f'{data[page][2]}: {price} {currency.upper()}',
                                      callback_data=ProductCallbackFactory(type="more",
                                                                           product_id=f"{data[page][1]}",
                                                                           category_id=f"{data[page][6]}",
                                                                           page_num=page).pack()))
    keyboard.row(InlineKeyboardButton(text=f"❤ {languages[lang]['added_to_fav']}" if in_fav
                                                else f"{languages[lang]['add_to_fav']}",
                                      callback_data=ProductCallbackFactory(type="to_favorites",
                                                                           product_id=f"{data[page][1]}",
                                                                           category_id=f"{data[page][6]}",
                                                                           page_num=page).pack()),
                 InlineKeyboardButton(text=f"🛒 {languages[lang]['added_to_cart']}" if in_cart
                                                else f"{languages[lang]['add_to_cart']}",
                                      callback_data=ProductCallbackFactory(type="to_cart",
                                                                           product_id=f"{data[page][1]}",
                                                                           category_id=f"{data[page][6]}",
                                                                           page_num=page).pack()))
    keyboard.row(InlineKeyboardButton(text='<<',
                                      callback_data=ProductCallbackFactory(
                                          type="nav",
                                          category_id=f"{data[page][6]}",
                                          page_num=0).pack()),
                 InlineKeyboardButton(text='<️',
                                      callback_data=ProductCallbackFactory(
                                          type="nav",
                                          category_id=f"{data[page][6]}",
                                          page_num=min(max(page - 1, 0), max_page)).pack()),
                 InlineKeyboardButton(text=f'{page + 1}/{max_page + 1}',
                                      callback_data=ProductCallbackFactory(
                                          type="mid",
                                          category_id=f"{data[page][6]}",).pack()),
                 InlineKeyboardButton(text='>',
                                      callback_data=ProductCallbackFactory(
                                          type="nav",
                                          category_id=f"{data[page][6]}",
                                          page_num=min(max(page + 1, 0), max_page)).pack()),
                 InlineKeyboardButton(text='>>',
                                      callback_data=ProductCallbackFactory(
                                          type="nav",
                                          category_id=f"{data[page][6]}",
                                          page_num=max_page).pack()))

    keyboard.row(InlineKeyboardButton(text=languages[lang]['back'],
                                      callback_data=ProductCallbackFactory(type="back").pack()),
                 InlineKeyboardButton(text=languages[lang]['main_menu'],
                                      callback_data=ProductCallbackFactory(type="back_to_main").pack()),
                 InlineKeyboardButton(text=languages[lang]['cart'],
                                      callback_data=ProductCallbackFactory(type="cart").pack()),
                 )

    return keyboard, info
