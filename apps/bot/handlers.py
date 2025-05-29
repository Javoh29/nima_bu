from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters.command import CommandStart
from aiogram.enums.parse_mode import ParseMode
from django.core.cache import cache
from apps.bot.keyboards import build_keyboard
from apps.bot.utils import generate_caption
from services.main.service import MainService
from services.olx.service import OlxService
from services.uzum.service import UzumService
import json
import logging

logging.basicConfig(level=logging.INFO)

router = Router()

services = {
    "OLX": OlxService,
    "Uzum Market": UzumService
}

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("✅ Xush kelibsiz!")

@router.message()
async def search_handler(message: Message):
    search_text = message.text
    async for main_schema in MainService().search(search_text):
        for index, item in enumerate(main_schema.items):
            show_more_data = None
            button_text = None
            if main_schema.offset + main_schema.limit < main_schema.total and index == main_schema.limit - 1:
                show_more_data = {
                    "offset": main_schema.offset + main_schema.limit,
                    "service_title": main_schema.service_title,
                    "text": search_text
                }
                button_text = f"{main_schema.service_title} dagi mahsulotlardan yana ko'rsatish"

            markup = build_keyboard(item.url, show_more_data, button_text)
            caption = generate_caption(main_schema.service_title, item)
            await message.answer_photo(photo=item.photo, caption=caption, reply_markup=markup, parse_mode=ParseMode.HTML)

@router.callback_query(F.data)
async def handle_show_more(callback: CallbackQuery):
    data = cache.get(callback.data)

    if not data:
        markup = callback.message.reply_markup
        if markup and markup.inline_keyboard:
            new_keyboard_rows = markup.inline_keyboard[:-1]
            new_markup = InlineKeyboardMarkup(inline_keyboard=new_keyboard_rows) if new_keyboard_rows else None
            await callback.message.edit_reply_markup(reply_markup=new_markup)
        return

    data = json.loads(data)
    service = services[data["service_title"]]()
    search_text = data["text"]
    main_schema = await service.search(text=search_text, offset=data["offset"])

    for index, item in enumerate(main_schema.items):
        show_more_data = None
        button_text = None
        if main_schema.offset + main_schema.limit < main_schema.total and index == main_schema.limit - 1:
            show_more_data = {
                "offset": main_schema.offset + main_schema.limit,
                "service_title": main_schema.service_title,
                "text": search_text
            }
            button_text = f"{main_schema.service_title} dagi mahsulotlardan yana ko'rsatish"

        markup = build_keyboard(item.url, show_more_data, button_text)
        caption = generate_caption(main_schema.service_title, item)
        await callback.message.answer_photo(photo=item.photo, caption=caption, reply_markup=markup, parse_mode=ParseMode.HTML)
