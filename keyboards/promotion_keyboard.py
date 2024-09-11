from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from db.sql import DataBase
from languages.languages import languages, ImagePath


db = DataBase('my_database.db')


class NewsCallbackFactory(CallbackData, prefix="news"):
    type: str
    product_id: Optional[int] = None
    page_num: Optional[int] = None


async def get_promotion_keyboard(page, user_id):

    keyboard = InlineKeyboardBuilder()

    data = await db.get_promotion()
    lang = await db.get_lang(user_id)
    lang = lang[0][0]

    max_page = len(data)-1
    page = min(page, max_page)

    info = None
    if data:
        in_cart = await db.get_count_in_cart(user_id, data[page][5])
        info = f'{data[page][0]} : -{data[page][1]}% on {data[page][4]}',  data[page][2]
        keyboard.row(InlineKeyboardButton(text=f"🛒 {languages[lang]['added_to_cart']}" if in_cart
                                                else f"{languages[lang]['add_to_cart']}",
                                          callback_data=NewsCallbackFactory(type="to_cart",
                                                                            product_id=f"{data[page][5]}",
                                                                            page_num=page).pack()))
        keyboard.row(InlineKeyboardButton(text='<<',
                                          callback_data=NewsCallbackFactory(
                                              type="nav",
                                              page_num=0).pack()),
                     InlineKeyboardButton(text='<',
                                          callback_data=NewsCallbackFactory(
                                              type="nav",
                                              page_num=min(max(page-1, 0), max_page)).pack()),
                     InlineKeyboardButton(text=f'{page+1}/{max_page+1}',
                                          callback_data=NewsCallbackFactory(
                                              type="mid").pack()),
                     InlineKeyboardButton(text='>',
                                          callback_data=NewsCallbackFactory(
                                              type="nav",
                                              page_num=min(max(page + 1, 0), max_page)).pack()),
                     InlineKeyboardButton(text='>>',
                                          callback_data=NewsCallbackFactory(
                                              type="nav",
                                              page_num=max_page).pack()))

    keyboard.row(InlineKeyboardButton(text=languages[lang]['back'],
                                      callback_data=NewsCallbackFactory(
                                          type="back").pack()))
    if not info:
        info = (languages[lang]["empty_promo"],
                f"{ImagePath}empty.png")
    return keyboard, info
