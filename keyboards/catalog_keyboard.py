
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.sql import DataBase
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from math import ceil
from languages.languages import languages


db = DataBase('my_database.db')


class CatalogCallbackFactory(CallbackData, prefix="catalog"):
    type: str
    category_id: Optional[int] = None
    page_num: Optional[int] = None


async def get_catalog_keyboard(page, user_id):

    keyboard = InlineKeyboardBuilder()

    data = await db.get_categories()
    lang = await db.get_lang(user_id)
    lang = lang[0][0]

    max_page = ceil(len(data)/2)

    for index, i in enumerate(data):
        if (page + 1)*2 > index >= page*2:
            keyboard.button(text=f'{i[0]}',
                            callback_data=CatalogCallbackFactory(type="category", category_id=f"{i[1]}"))

    keyboard.row(InlineKeyboardButton(text='<<',
                                      callback_data=CatalogCallbackFactory(
                                          type="nav",
                                          page_num=0).pack()),
                 InlineKeyboardButton(text='<',
                                      callback_data=CatalogCallbackFactory(
                                          type="nav",
                                          page_num=min(max(page-1, 0), max_page-1)).pack()),
                 InlineKeyboardButton(text=f'{page+1}/{max_page}',
                                      callback_data=CatalogCallbackFactory(type="mid").pack()),
                 InlineKeyboardButton(text='>️',
                                      callback_data=CatalogCallbackFactory(
                                          type="nav",
                                          page_num=min(max(page+1, 0), max_page-1)).pack()),
                 InlineKeyboardButton(text='>>',
                                      callback_data=CatalogCallbackFactory(
                                          type="nav",
                                          page_num=max_page).pack()))

    keyboard.row(InlineKeyboardButton(text=languages[lang]['back'],
                                      callback_data=CatalogCallbackFactory(type="back").pack()))

    return keyboard
