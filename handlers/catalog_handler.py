from aiogram.types import CallbackQuery

from aiogram import F
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest

from keyboards.catalog_keyboard import CatalogCallbackFactory, get_catalog_keyboard
from keyboards.main_keyboard import get_main_keyboard
from keyboards.products_keyboard import gen_products_keyboard
from languages.translator import to_user_lang, ImagePath

from db.sql import DataBase
from main import dp, bot


db = DataBase('my_database.db')


@dp.callback_query(CatalogCallbackFactory.filter(F.type == "category"))
async def catalog_nav(callback: CallbackQuery, callback_data: CatalogCallbackFactory):

    keyboard, (desc, photo) = await gen_products_keyboard(callback_data.category_id,
                                                          callback.from_user.id,
                                                          0)
    lang = await db.get_lang(callback.from_user.id)
    lang = lang[0][0]
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(
                media=FSInputFile(photo),
                caption=to_user_lang(desc, lang)),
            reply_markup=keyboard.as_markup())
    except TelegramBadRequest as e:
        pass


@dp.callback_query(CatalogCallbackFactory.filter(F.type == "nav"))
async def goods(callback: CallbackQuery, callback_data: CatalogCallbackFactory):

    keyboard = await get_catalog_keyboard(callback_data.page_num,
                                          callback.from_user.id)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(
                media=FSInputFile(f"{ImagePath}Catalog.jpg"),
                caption=''),
            reply_markup=keyboard.as_markup())
    except TelegramBadRequest as e:
        pass


@dp.callback_query(CatalogCallbackFactory.filter(F.type == "back"))
async def goods(callback: CallbackQuery, callback_data: CatalogCallbackFactory):

    keyboard = await get_main_keyboard(callback.from_user.id)

    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(f"{ImagePath}Catalog.jpg"),
            caption=''),
        reply_markup=keyboard.as_markup()
    )
