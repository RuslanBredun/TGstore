from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton

from db.sql import DataBase
from main import dp, bot
from aiogram import F
from aiogram.exceptions import TelegramBadRequest

from keyboards.settings_keyboard import SettingsCallbackFactory, \
    get_currency_keyboard, get_settings_keyboard, get_set_lang_keyboard
from keyboards.main_keyboard import get_main_keyboard
from languages.languages import ImagePath

from aiogram.types import FSInputFile, InputMediaPhoto

db = DataBase('my_database.db')


@dp.callback_query(SettingsCallbackFactory.filter(F.type == "currency"))
async def currency(callback: CallbackQuery, callback_data: SettingsCallbackFactory):

    keyboard = await get_currency_keyboard(callback.from_user.id)

    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(f"{ImagePath}settings.webp"),
            caption=''),
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(SettingsCallbackFactory.filter(F.type == "language"))
async def language(callback: CallbackQuery, callback_data: SettingsCallbackFactory):

    keyboard = await get_set_lang_keyboard(callback.from_user.id)

    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(f"{ImagePath}settings.webp"),
            caption=''),
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(SettingsCallbackFactory.filter(F.type == "back"))
async def back(callback: CallbackQuery, callback_data: SettingsCallbackFactory):

    keyboard = await get_main_keyboard(callback.from_user.id)

    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(f"{ImagePath}main.jpg"),
            caption=''),
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(SettingsCallbackFactory.filter(F.type == "set_currency"))
async def set_currency(callback: CallbackQuery, callback_data: SettingsCallbackFactory):

    await db.set_currency(callback.from_user.id, callback_data.currency)

    keyboard = await get_currency_keyboard(callback.from_user.id)

    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(f"{ImagePath}settings.webp"),
            caption=''),
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(SettingsCallbackFactory.filter(F.type == "set_lang"))
async def set_lang(callback: CallbackQuery, callback_data: SettingsCallbackFactory):

    await db.set_lang(callback.from_user.id, callback_data.lang)

    keyboard = await get_set_lang_keyboard(callback.from_user.id)

    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(f"{ImagePath}settings.webp"),
            caption=''),
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(SettingsCallbackFactory.filter(F.type == "back_settings"))
async def back_settings(callback: CallbackQuery, callback_data: SettingsCallbackFactory):

    keyboard = await get_settings_keyboard(callback.from_user.id)

    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(f"{ImagePath}settings.webp"),
            caption=''),
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(SettingsCallbackFactory.filter(F.type == "set_init_lang"))
async def set_init_lang(callback: CallbackQuery, callback_data: SettingsCallbackFactory):
    await db.set_lang(callback.from_user.id, callback_data.lang)

    keyboard = await get_main_keyboard(callback.from_user.id)

    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,media=InputMediaPhoto(
            media=FSInputFile(f"{ImagePath}main.jpg"),
            caption=''),
        reply_markup=keyboard.as_markup()
    )