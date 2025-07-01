import json
from django.core.cache import cache
from uuid import uuid4
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def build_keyboard(item_url, show_more_data=None, button_text=None):
    keyboard = [[InlineKeyboardButton(text="Открыть", url=item_url)]]
    if show_more_data:
        uid = str(uuid4())
        cache.set(uid, json.dumps(show_more_data), timeout=86400)
        keyboard.append([
            InlineKeyboardButton(
                text=button_text,
                callback_data=uid
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# def build_keyboard(item_url, show_more_data=None, button_text=None):
#     keyboard = [[InlineKeyboardButton(text="Ochish", url=item_url)]]
#     if show_more_data:
#         uid = str(uuid4())
#         cache.set(uid, json.dumps(show_more_data), timeout=86400)
#         keyboard.append([
#             InlineKeyboardButton(
#                 text=button_text,
#                 callback_data=uid
#             )
#         ])
#     return InlineKeyboardMarkup(inline_keyboard=keyboard)