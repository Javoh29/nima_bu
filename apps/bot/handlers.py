from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters.command import CommandStart
from aiogram.enums.parse_mode import ParseMode
from django.core.cache import cache
from services.main.service import MainService
from services.main.schema import MainSchema
from services.olx.service import OlxService
from services.uzum.service import UzumService
import json
import logging
from uuid import uuid4

logging.basicConfig(level=logging.INFO)

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("✅ Xush kelibsiz!")

@router.message()
async def search_handler(message: Message):
    search_text = message.text
    async for main_schema in MainService().search(search_text):
        for index, item in enumerate(main_schema.items):
            inline_keyboard = [
                [
                    InlineKeyboardButton(text="Ochish", url=item.url)
                ]
            ]
            if main_schema.offset + main_schema.limit < main_schema.total and index == main_schema.limit - 1:
                uid = str(uuid4())
                data = json.dumps({"offset": main_schema.offset+main_schema.limit, "service_title": main_schema.service_title, "text": search_text})
                cache.set(uid, data, timeout=86400)
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(
                            text=f"{main_schema.service_title} dagi mahsulotlardan yana ko'rsatish",
                            callback_data=uid
                        )
                    ]
                )
            inline_keyboard_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            caption = (
                f"<b>{main_schema.service_title}:</b> {item.title}\n"
                f"Narxi: <b>{int(item.sell_price):,} so'm</b> <s>{f"{item.full_price:,} so'm" if item.full_price else ""}</s>".replace(",", " ")
            )

            await message.answer_photo(photo=item.photo, caption=caption, reply_markup=inline_keyboard_markup, parse_mode=ParseMode.HTML)


@router.callback_query(F.data)
async def handle_show_more(callback: CallbackQuery):
    services = {
        "OLX": OlxService,
        "Uzum Market": UzumService
    }
    print(callback.inline_message_id)
    data = cache.get(callback.data)
    if not data:
        markup = callback.message.reply_markup

        if markup and markup.inline_keyboard:
            # Flatten all buttons into a list
            new_keyboard_rows = markup.inline_keyboard[:-1]  # Remove last row

        # If there are still rows left, rebuild keyboard
            new_markup = InlineKeyboardMarkup(inline_keyboard=new_keyboard_rows) if new_keyboard_rows else None
            await callback.message.edit_reply_markup(reply_markup=new_markup)
            return

    data = json.loads(data)
    service = services[data["service_title"]]()
    search_text = data["text"]
    main_schema = await service.search(text=search_text, offset=data["offset"])
    for index, item in enumerate(main_schema.items):
        inline_keyboard = [
            [
                InlineKeyboardButton(text="Ochish", url=item.url)
            ]
        ]
        if main_schema.offset + main_schema.limit < main_schema.total and index == main_schema.limit - 1:
            uid = str(uuid4())
            data = json.dumps({"offset": main_schema.offset+main_schema.limit, "service_title": main_schema.service_title, "text": search_text})
            cache.set(uid, data, timeout=86400)
            inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        text=f"{main_schema.service_title} dagi mahsulotlardan yana ko'rsatish",
                        callback_data=uid
                    )
                ]
            )
        inline_keyboard_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        caption = (
            f"<b>{main_schema.service_title}:</b> {item.title}\n"
            f"Narxi: <strong>{int(item.sell_price):,} so'm</strong> <s>{f"{item.full_price:,} so'm" if item.full_price else ""}</s>".replace(",", " ")
        )
        await callback.message.answer_photo(photo=item.photo, caption=caption, reply_markup=inline_keyboard_markup, parse_mode=ParseMode.HTML)

