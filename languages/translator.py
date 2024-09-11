import httpcore
from typing import Any
setattr(httpcore, 'SyncHTTPTransport', Any)

from googletrans import Translator
from db.sql import DataBase

db = DataBase('my_database.db')

# Create an instance of the Translator class
translator = Translator()


def to_bot_lang(msg: str) -> str:

    res = translator.translate(msg, dest='en')
    print(type(res))
    return res.text


def to_user_lang(msg: str, lang) -> str:
    res = translator.translate(msg, dest=lang)
    print(type(res))
    return res.text
