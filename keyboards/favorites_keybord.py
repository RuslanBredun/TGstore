from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from db.sql import DataBase
from languages.languages import languages, ImagePath

db = DataBase('my_database.db')


class FavoritesCallbackFactory(CallbackData, prefix="favorites"):
    type: str
    product_id: Optional[int] = None
    category_id: Optional[int] = None
    page_num: Optional[int] = None


async def get_favorites_keyboard(page, user_id):

    keyboard = InlineKeyboardBuilder()

    data = await db.get_favorites(user_id)
    lang = await db.get_lang(user_id)
    lang = lang[0][0]

    max_page = len(data)-1
    page = min(page, max_page)

    info = None
    if data:
        info = data[page][4], data[page][5]
        keyboard.button(text=f'{data[page][0]}',
                        callback_data=FavoritesCallbackFactory(type="cart"))
        keyboard.row(InlineKeyboardButton(text='🛒',
                                          callback_data=FavoritesCallbackFactory(type="add",
                                                                                 product_id=f"{data[page][3]}",
                                                                                 category_id=f"{data[page][1]}",
                                                                                 page_num=page).pack()),
                     InlineKeyboardButton(text='❌',
                                          callback_data=FavoritesCallbackFactory(type="del",
                                                                                 product_id=f"{data[page][3]}",
                                                                                 category_id=f"{data[page][1]}",
                                                                                 page_num=page).pack()))
        keyboard.row(InlineKeyboardButton(text='<<',
                                          callback_data=FavoritesCallbackFactory(
                                              type="nav",
                                              page_num=0).pack()),
                     InlineKeyboardButton(text='<',
                                          callback_data=FavoritesCallbackFactory(
                                              type="nav",
                                              page_num=min(max(page-1, 0), max_page)).pack()),
                     InlineKeyboardButton(text=f'{page+1}/{max_page+1}',
                                          callback_data=FavoritesCallbackFactory(
                                              type="mid").pack()),
                     InlineKeyboardButton(text='>',
                                          callback_data=FavoritesCallbackFactory(
                                              type="nav",
                                              page_num=min(max(page + 1, 0), max_page)).pack()),
                     InlineKeyboardButton(text='>>',
                                          callback_data=FavoritesCallbackFactory(
                                              type="nav",
                                              page_num=max_page).pack()))

    keyboard.row(InlineKeyboardButton(text=languages[lang]['back'],
                                      callback_data=FavoritesCallbackFactory(
                                          type="back").pack()))
    if not info:
        info = (languages[lang]["empty_fav"],
                f"{ImagePath}empty.png")
    return keyboard, info
