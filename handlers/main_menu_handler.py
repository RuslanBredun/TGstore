from aiogram.types import CallbackQuery

from main import dp, bot
from aiogram import F

from keyboards.main_keyboard import MainMenuCallbackFactory

from keyboards.catalog_keyboard import get_catalog_keyboard
from keyboards.cart_keyboard import get_cart_keyboard
from keyboards.favorites_keybord import get_favorites_keyboard
from keyboards.settings_keyboard import get_settings_keyboard, get_init_lang_keyboard
from keyboards.promotion_keyboard import get_promotion_keyboard
from keyboards.ai_keyboard import get_ai_keyboard, AIState
from languages.translator import to_user_lang, ImagePath
from aiogram.fsm.context import FSMContext

from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.types import Message
from aiogram.filters import Command

from db.sql import DataBase
from languages.languages import languages

db = DataBase('my_database.db')


@dp.message(Command("start"))
async def cmd_start(message: Message):
    try:
        await db.add_users(message.from_user.id, message.chat.first_name)
    except Exception as e:
        pass
    finally:
        keyboard = await get_init_lang_keyboard(message.from_user.id)
        image = FSInputFile(f"{ImagePath}main.jpg")
        await message.answer_photo(
            image,
            caption=languages["en"]["choose_language"],
            reply_markup=keyboard.as_markup()
        )


@dp.callback_query(MainMenuCallbackFactory.filter(F.type == "catalog"))
async def main_catalog(callback: CallbackQuery, callback_data: MainMenuCallbackFactory):

    keyboard = await get_catalog_keyboard(0, callback.from_user.id)

    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(f"{ImagePath}Catalog.jpg"),
            caption=''),
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(MainMenuCallbackFactory.filter(F.type == "cart"))
async def main_cart(callback: CallbackQuery, callback_data: MainMenuCallbackFactory):

    keyboard, (desc, photo) = await get_cart_keyboard(0, callback.from_user.id)

    lang = await db.get_lang(callback.from_user.id)
    lang = lang[0][0]
    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(photo),
            caption=to_user_lang(desc, lang)),
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(MainMenuCallbackFactory.filter(F.type == "favorites"))
async def main_favorites(callback: CallbackQuery, callback_data: MainMenuCallbackFactory):

    keyboard, (desc, photo) = await get_favorites_keyboard(0, callback.from_user.id)

    lang = await db.get_lang(callback.from_user.id)
    lang = lang[0][0]
    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(photo),
            caption=to_user_lang(desc, lang)),
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(MainMenuCallbackFactory.filter(F.type == "promotion"))
async def main_news(callback: CallbackQuery, callback_data: MainMenuCallbackFactory):

    keyboard, (desc, photo) = await get_promotion_keyboard(0, callback.from_user.id)

    lang = await db.get_lang(callback.from_user.id)
    lang = lang[0][0]
    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(photo),
            caption=to_user_lang(desc, lang)),
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(MainMenuCallbackFactory.filter(F.type == "settings"))
async def main_settings(callback: CallbackQuery, callback_data: MainMenuCallbackFactory):

    keyboard = await get_settings_keyboard(callback.from_user.id)

    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(f"{ImagePath}settings.webp"),
            caption=''),
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(MainMenuCallbackFactory.filter(F.type == "ai"))
async def main_ai(callback: CallbackQuery, callback_data: MainMenuCallbackFactory, state: FSMContext):

    keyboard = await get_ai_keyboard(callback.from_user.id)
    lang = await db.get_lang(callback.from_user.id)
    lang = lang[0][0]
    await state.set_state(AIState.ai)

    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(f"{ImagePath}ai.webp"))
    )
    await callback.message.answer(
        text=to_user_lang('Hello, I am your consultant. How I can help you?', lang),
        reply_markup=keyboard.as_markup(resize_keyboard=True),
    )
