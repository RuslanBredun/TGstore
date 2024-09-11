from aiogram.types import CallbackQuery

from db.sql import DataBase
from main import dp, bot
from aiogram import F
from aiogram.exceptions import TelegramBadRequest

from keyboards.promotion_keyboard import NewsCallbackFactory, get_promotion_keyboard
from keyboards.main_keyboard import get_main_keyboard
from languages.translator import to_user_lang, ImagePath

from aiogram.types import FSInputFile, InputMediaPhoto

db = DataBase('my_database.db')


@dp.callback_query(NewsCallbackFactory.filter(F.type == "nav"))
async def products_nav(callback: CallbackQuery, callback_data: NewsCallbackFactory):

    keyboard, (desc, photo) = await get_promotion_keyboard(callback_data.page_num,
                                                           callback.from_user.id)
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


@dp.callback_query(NewsCallbackFactory.filter(F.type == "back"))
async def back(callback: CallbackQuery, callback_data: NewsCallbackFactory):

    keyboard = await get_main_keyboard(callback.from_user.id)

    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(f"{ImagePath}Catalog.jpg"),
            caption=''),
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(NewsCallbackFactory.filter(F.type == "to_cart"))
async def products_to_cart(callback: CallbackQuery, callback_data: NewsCallbackFactory):

    product_id = callback_data.product_id

    count_in_cart = await db.get_count_in_cart(callback.from_user.id, product_id)
    count_in_stock = await db.get_count_in_stock(product_id)

    lang = await db.get_lang(callback.from_user.id)
    lang = lang[0][0]
    if count_in_stock[0][0] == 0:
        await callback.answer(to_user_lang('Товара нет в наличии :(', lang))
        return 0
    elif not count_in_cart or count_in_cart[0][0] == 0:
        await db.add_to_cart(callback.from_user.id, product_id)
        await callback.answer(to_user_lang('Добавлено!', lang))
    else:
        await callback.answer(to_user_lang('Товар уже добавлен!', lang))

    keyboard, (desc, photo) = await get_promotion_keyboard(callback_data.page_num,
                                                           callback.from_user.id)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(
                media=FSInputFile(photo),
                caption=desc),
            reply_markup=keyboard.as_markup())
    except TelegramBadRequest as e:
        pass