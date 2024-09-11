import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

API_TOKEN = '6928202299:AAGzhFIZULHsU3SHXPbYsVZJhfPY7WvG_aY'


# class SomeMiddleware(BaseMiddleware):
#     async def __call__(
#         self,
#         handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#         event: TelegramObject,
#         data: Dict[str, Any]
#     ) -> Any:
#         # print("Before handler")
#         # print("event ", event)
#         # print("data ", data["event_from_user"].language_code)
#         result = await handler(event, data)
#         # print("After handler")
#         return result


bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    from handlers import dp
    # dp.message.middleware(SomeMiddleware())
    # dp.callback_query.middleware(SomeMiddleware())
    await dp.start_polling(bot)

if __name__ == '__main__':
    print("Hello")
    asyncio.run(main())
