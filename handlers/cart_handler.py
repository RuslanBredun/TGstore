from aiogram.types import CallbackQuery

from db.sql import DataBase
from main import dp, bot
from main import dp
from aiogram import F
from aiogram.exceptions import TelegramBadRequest

from keyboards.main_keyboard import get_main_keyboard
from keyboards.cart_keyboard import CartCallbackFactory, get_cart_keyboard
from languages.translator import to_user_lang, ImagePath

from aiogram.types import FSInputFile, InputMediaPhoto, \
    LabeledPrice, PreCheckoutQuery, ShippingQuery, ShippingOption, Message
from currency_converter import CurrencyConverter
converter = CurrencyConverter()


db = DataBase('my_database.db')


@dp.callback_query(CartCallbackFactory.filter(F.type == "back"))
async def back(callback: CallbackQuery, callback_data: CartCallbackFactory):

    keyboard = await get_main_keyboard(callback.from_user.id)

    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(f"{ImagePath}Catalog.jpg"),
            caption=''),
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(CartCallbackFactory.filter(F.type == "nav"))
async def products_nav(callback: CallbackQuery, callback_data: CartCallbackFactory):

    keyboard, (desc, photo) = await get_cart_keyboard(callback_data.page_num,
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


@dp.callback_query(CartCallbackFactory.filter(F.type == "minus"))
async def minus(callback: CallbackQuery, callback_data: CartCallbackFactory):

    count_in_cart = await db.get_count_in_cart(callback.from_user.id,
                                               callback_data.product_id)
    lang = await db.get_lang(callback.from_user.id)
    lang = lang[0][0]
    if not count_in_cart or count_in_cart[0][0] == 0:
        await callback.answer(to_user_lang('Товар в  корзине отсутсвует!', lang))
        return 0
    elif count_in_cart[0][0] == 1:
        await db.remove_one_item(callback_data.product_id, callback.from_user.id)
        await callback.answer(to_user_lang('Удалено!', lang))
    else:
        await db.change_count(count_in_cart[0][0] - 1, callback_data.product_id, callback.from_user.id)
        await callback.answer(to_user_lang('Удалено!', lang))

    keyboard, (desc, photo) = await get_cart_keyboard(callback_data.page_num,
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


@dp.callback_query(CartCallbackFactory.filter(F.type == "plus"))
async def plus(callback: CallbackQuery, callback_data: CartCallbackFactory):

    count_in_cart = await db.get_count_in_cart(callback.from_user.id, callback_data.product_id)
    count_in_stock = await db.get_count_in_stock(callback_data.product_id)
    lang = await db.get_lang(callback.from_user.id)
    lang = lang[0][0]
    if not count_in_cart or count_in_cart[0][0] == 0:
        await db.add_to_cart(callback.from_user.id, callback_data.product_id)
        await callback.answer(to_user_lang('Добавил!', lang))
    elif count_in_cart[0][0] < count_in_stock[0][0]:
        await db.change_count(count_in_cart[0][0] + 1, callback_data.product_id, callback.from_user.id)
    else:
        await callback.answer(to_user_lang('Больше нет в наличии', lang))
        return 0

    keyboard, (desc, photo) = await get_cart_keyboard(callback_data.page_num,
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


@dp.callback_query(CartCallbackFactory.filter(F.type == "del"))
async def delete(callback: CallbackQuery, callback_data: CartCallbackFactory):

    count_in_cart = await db.get_count_in_cart(callback.from_user.id,
                                               callback_data.product_id)
    lang = await db.get_lang(callback.from_user.id)
    lang = lang[0][0]

    if not count_in_cart:
        await callback.answer(to_user_lang('Товар в корзине отсутствует!', lang))
        return 0
    else:
        await db.remove_one_item(callback_data.product_id, callback.from_user.id)
        await callback.answer(to_user_lang('Удалено!', lang))

    keyboard, (desc, photo) = await get_cart_keyboard(callback_data.page_num,
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


@dp.callback_query(CartCallbackFactory.filter(F.type == "buy"))
async def delete(callback: CallbackQuery, callback_data: CartCallbackFactory):
    cart = await db.get_cart(callback.message.chat.id)

    currency = await db.get_currency(callback.from_user.id)
    currency = currency[0][0]

    prices = []
    for product in cart:
        print(round(product[2] * round(converter.convert(product[4], 'USD', currency.upper()), 2) * 100))
        prices.append(LabeledPrice(
            label=f"{product[2]} x {product[0]}",
            amount=round(product[2] * round(converter.convert(product[4], 'USD', currency.upper()), 2) * 100)  # price * 100
        ))
        await db.add_to_orders(callback.id,
                               product[3],
                               product[2],
                               "pre_checkout",
                               callback.from_user.id)

    await bot.send_invoice(callback.message.chat.id,
                           title='Your order',
                           description='Description',
                           provider_token="284685063:TEST:OTRmMWRmMWE4Nzhj",
                           currency=currency,
                           is_flexible=True,
                           need_shipping_address=True,
                           need_email=False,
                           # max_tip_amount=5000,
                           # suggested_tip_amounts=[1000, 2000, 4000], # max 4 elements
                           prices=prices,
                           start_parameter='example',
                           payload='some_invoice')


@dp.shipping_query()
async def shipping_process(shipping_query: ShippingQuery):
    lang = await db.get_lang(shipping_query.from_user.id)
    lang = lang[0][0]
    if shipping_query.shipping_address.country_code == 'RU':
        return await bot.answer_shipping_query(
            shipping_query.id,
            ok=False,
            error_message=to_user_lang('Сюда не доставляем!', lang)
        )
    shipping_options = [ShippingOption(id='regular',
                                       title=to_user_lang('Обычная доставка', lang),
                                       prices=[LabeledPrice(label=to_user_lang('Обычная доставка', lang),amount=9900)])]
    fast_shipping_option = ShippingOption(id='fast',
                                       title=to_user_lang('Быстрая доставка', lang),
                                       prices=[LabeledPrice(label=to_user_lang('Быстрая доставка', lang),amount=99000)])

    if shipping_query.shipping_address.country_code == 'UA':
        shipping_options.append(fast_shipping_option)

    await bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
        shipping_options=shipping_options
    )


@dp.pre_checkout_query()
async def cmd_pay(pre_checkout: PreCheckoutQuery):

    order_id = await db.get_last_order(pre_checkout.from_user.id)
    order_id = order_id[0][0]
    info = pre_checkout.order_info.shipping_address
    address = f"{info.country_code} - {info.state} - {info.city} - {info.street_line1} - {info.street_line2} - {info.post_code}"
    await db.change_order_shipment(order_id, pre_checkout.shipping_option_id, address)

    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)


@dp.message(F.successful_payment)
async def on_successful_payment(message: Message):

    order_id = await db.get_last_order(message.from_user.id)
    order_id = order_id[0][0]
    await db.change_order_status(order_id, "paid")

    await db.empty_cart(message.from_user.id)

    keyboard = await get_main_keyboard(message.from_user.id)
    await message.answer_photo(
        FSInputFile(f"{ImagePath}Catalog.jpg"),
        caption='',
        reply_markup=keyboard.as_markup()
    )
