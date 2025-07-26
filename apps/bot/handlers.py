from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters.command import CommandStart
from aiogram.enums.parse_mode import ParseMode
from django.core.cache import cache
from apps.bot.schema import TextShowMoreSchema, ImageShowMoreSchema
from apps.bot.keyboards import build_keyboard
from apps.bot.utils import generate_caption
from apps.bot.filters import PhotoCallbackFilter, TextCallbackFilter, RemoveButtonCallbackFilter
from services.main.service import MainService
from services.iswb.service import ISWBService
from services.main.schema import MainItemSchema, MainSchema

from services.olx.service import OlxService
from services.uzum.service import UzumService
from uuid import uuid4
from django.conf import settings
import json
import logging
import os
import asyncio
logging.basicConfig(level=logging.INFO)

router = Router()

services = {
    "OLX": OlxService(),
    "Uzum Market": UzumService(),
    "WildBerries": ISWBService(),
}


# @router.message(CommandStart())
# async def start_handler(message: Message):
#     await message.answer("✅ Xush kelibsiz!")

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("✅ Xush kelibsiz!\n\n")

@router.message(F.photo)
async def photo_handler(message: Message, bot: Bot):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    ext = os.path.splitext(file.file_path)[-1]
    file_path = f"image_{uuid4().hex}{ext}"
    saved_dir = os.path.join(settings.MEDIA_ROOT, "photos", "bot")
    os.makedirs(saved_dir, exist_ok=True)
    saved_path = os.path.join(saved_dir, file_path)
    service = ISWBService()
    await bot.download_file(file.file_path, saved_path)
    main_schema: MainSchema = await service.search(image_path=saved_path)
    for index, item in enumerate(main_schema.items):
        show_more_data = None
        button_text = None
        if main_schema.offset + main_schema.limit < main_schema.total and index == main_schema.limit - 1:
            show_more_data = ImageShowMoreSchema(
                image_path=saved_path,
                offset=main_schema.offset + main_schema.limit,
                service_title=main_schema.service_title
            )
            button_text = f"{main_schema.service_title} dagi mahsulotlardan yana ko'rsatish"

        markup = build_keyboard(item.url, show_more_data, button_text)
        caption = generate_caption(main_schema.service_title, item)
        await message.answer_photo(photo=item.photo, caption=caption, reply_markup=markup, parse_mode=ParseMode.HTML)    # await message.answer_photo(photo=schema.photo, caption=caption, reply_markup=markup, parse_mode=ParseMode.HTML)



@router.message(F.text)
async def search_handler(message: Message):
    search_text = message.text
    async for main_schema in MainService().search(search_text):
        for index, item in enumerate(main_schema.items):
            show_more_data = None
            button_text = None
            if main_schema.offset + main_schema.limit < main_schema.total and index == main_schema.limit - 1:
                show_more_data = TextShowMoreSchema(
                    text=search_text,
                    offset=main_schema.offset + main_schema.limit,
                    service_title=main_schema.service_title
                )
                button_text = f"{main_schema.service_title} dagi mahsulotlardan yana ko'rsatish"

            markup = build_keyboard(item.url, show_more_data, button_text)
            caption = generate_caption(main_schema.service_title, item)
            await message.answer_photo(photo=item.photo, caption=caption, reply_markup=markup, parse_mode=ParseMode.HTML)
            

@router.callback_query(RemoveButtonCallbackFilter())
async def remove_button_handler(callback: CallbackQuery):
    markup = callback.message.reply_markup
    if markup and markup.inline_keyboard:
        new_keyboard_rows = markup.inline_keyboard[:-1]
        new_markup = InlineKeyboardMarkup(inline_keyboard=new_keyboard_rows) if new_keyboard_rows else None
        await callback.message.edit_reply_markup(reply_markup=new_markup)
    return

@router.callback_query(TextCallbackFilter())
async def text_callback_handler(callback: CallbackQuery):
    json = cache.get(callback.data)
    data = TextShowMoreSchema.model_validate_json(json)
    search_text = data.text
    service = services[data.service_title]
    main_schema = await service.search(text=search_text, offset=data.offset)

    for index, item in enumerate(main_schema.items):
        show_more_data = None
        button_text = None
        if main_schema.offset + main_schema.limit < main_schema.total and index == main_schema.limit - 1:
            show_more_data = TextShowMoreSchema(
                text=search_text, 
                offset=main_schema.offset + main_schema.limit, 
                service_title=main_schema.service_title
            )
            button_text = f"{main_schema.service_title} dagi mahsulotlardan yana ko'rsatish"

        markup = build_keyboard(item.url, show_more_data, button_text)
        caption = generate_caption(main_schema.service_title, item)
        await callback.message.answer_photo(photo=item.photo, caption=caption, reply_markup=markup, parse_mode=ParseMode.HTML)
    return

@router.callback_query(PhotoCallbackFilter())
async def photo_callback_handler(callback: CallbackQuery):
    json = cache.get(callback.data)
    data = ImageShowMoreSchema.model_validate_json(json)
    service = ISWBService()
    main_schema = await service.search(image_path=data.image_path, offset=data.offset)

    for index, item in enumerate(main_schema.items):
        show_more_data = None
        button_text = None
        if main_schema.offset + main_schema.limit < main_schema.total and index == main_schema.limit - 1:
            show_more_data = ImageShowMoreSchema(
                image_path=data.image_path,
                offset=main_schema.offset + main_schema.limit,
                service_title=main_schema.service_title
            )
            button_text = f"{main_schema.service_title} dagi mahsulotlardan yana ko'rsatish"

        markup = build_keyboard(item.url, show_more_data, button_text, search_type=data.search_type)
        caption = generate_caption(main_schema.service_title, item)
        await callback.message.answer_photo(photo=item.photo, caption=caption, reply_markup=markup, parse_mode=ParseMode.HTML)
    return
# @router.callback_query()
# async def handle_show_more(callback: CallbackQuery):
#     data = cache.get(callback.data)

#     if not data:
#         markup = callback.message.reply_markup
#         if markup and markup.inline_keyboard:
#             new_keyboard_rows = markup.inline_keyboard[:-1]
#             new_markup = InlineKeyboardMarkup(inline_keyboard=new_keyboard_rows) if new_keyboard_rows else None
#             await callback.message.edit_reply_markup(reply_markup=new_markup)
#         return

#     if callback.data.startswith("text_"):
#         data = TextShowMoreSchema.model_validate_json(data)
#         search_text = data.text
#         main_schema = await service.search(text=search_text, offset=data.offset)
#     elif callback.data.startswith("image_"):
#         data = ImageShowMoreSchema.model_validate_json(data)
#         main_schema = await service.search(text=search_text, offset=data.offset)
#     service = services[data.service_title]
    
    

#     for index, item in enumerate(main_schema.items):
#         show_more_data = None
#         button_text = None
#         if main_schema.offset + main_schema.limit < main_schema.total and index == main_schema.limit - 1:
#             show_more_data = TextShowMoreSchema(
#                 text=search_text, 
#                 offset=main_schema.offset + main_schema.limit, 
#                 service_title=main_schema.service_title
#             )
#             button_text = f"{main_schema.service_title} dagi mahsulotlardan yana ko'rsatish"

#         markup = build_keyboard(item.url, show_more_data, button_text)
#         caption = generate_caption(main_schema.service_title, item)
#         await callback.message.answer_photo(photo=item.photo, caption=caption, reply_markup=markup, parse_mode=ParseMode.HTML)

