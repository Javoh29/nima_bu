from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters.command import CommandStart
from aiogram.enums.parse_mode import ParseMode
from django.core.cache import cache
from apps.bot.keyboards import build_keyboard
from apps.bot.utils import generate_caption
from services.main.service import MainService
from services.main.schema import MainItemSchema
from services.olx.service import OlxService
from services.uzum.service import UzumService
import json
import logging
import os
import asyncio

logging.basicConfig(level=logging.INFO)

router = Router()

services = {
    "OLX": OlxService,
    "Uzum Market": UzumService
}

uzum_data = [
    {
    "id": 680851,
    "url": "https://uzum.uz/uz/product/680851?utm_source=sharing&utm_medium=product_page_android&utm_campaign=native",
    "photo": "https://images.uzum.uz/d1ef5vgs9rf9j55t4p7g/t_product_540_high.jpg",
    "full_price": 6095000,
    "sell_price": 2229000,
    "title": "Садовая воздуходувка-пылесос Bosch UniversalGardenTidy 3000, 1.8 кВт, 41 л"
    },
    {
    "id": 1194006,
    "url": "https://uzum.uz/uz/product/1194006?utm_source=sharing&utm_medium=product_page_android&utm_campaign=native",
    "photo": "https://images.uzum.uz/cue9oslht56ksubgm340/t_product_540_high.jpg",
    "full_price": 1200000,
    "sell_price": 269000,
    "title": "Турбо фен воздуходувка на все случаи жизни, сушилка, вентилятор"
    },
    {
    "id": 1714751,
    "url": "https://uzum.uz/uz/product/1714751?utm_source=sharing&utm_medium=product_page_android&utm_campaign=native",
    "photo": "https://images.uzum.uz/d0jhl8on274j5scn22ng/t_product_540_high.jpg",
    "full_price": 400000,
    "sell_price": 245000,
    "title": "Турбо-фен воздуходувка, аккумуляторный, на все случаи жизни"
    },
    {
    "id": 1105550,
    "url": "https://uzum.uz/uz/product/1105550?utm_source=sharing&utm_medium=product_page_android&utm_campaign=native",
    "photo": "https://images.uzum.uz/cpvqi6b6eisq2rke0cu0/t_product_540_high.jpg",
    "full_price": 1000000,
    "sell_price": 599900,
    "title": "Аккумуляторная воздуходувка, 5,6 куб. метр/мин, 19000 об/мин, 50-60 Гц"
    },
    {
    "id": 1562959,
    "url": "https://uzum.uz/uz/product/1562959?utm_source=sharing&utm_medium=product_page_android&utm_campaign=native",
    "photo": "https://images.uzum.uz/cuvhj0ei4n36ls3ru1c0/t_product_540_high.jpg",
    "full_price": 799000,
    "sell_price": 329000,
    "title": "Воздуходувка ультра-мощная, аккумуляторная"
    },
    {
    "id": 1225438,
    "url": "https://uzum.uz/uz/product/1225438?utm_source=sharing&utm_medium=product_page_android&utm_campaign=native",
    "photo": "https://images.uzum.uz/crq2fckhug2lhicofe5g/t_product_540_high.jpg",
    "full_price": 850000,
    "sell_price": 210000,
    "title": "Электрическая воздуходувка Biyoti BYT-EB01"
    }
]

wb_data = [
    {
        "id": 385704855,
        "url": "https://www.wildberries.ru/catalog/385704855/detail.aspx",
        "photo": "https://alm-basket-cdn-01.geobasket.ru/vol3857/part385704/385704855/images/big/1.webp",
        "full_price": 564030000,
        "sell_price": 310420000,
        "title": "Воздуходувка 125 B Blower бензиновая"
    },
    {
        "id": 205694185,
        "url": "https://www.wildberries.ru/catalog/205694185/detail.aspx",
        "photo": "https://alm-basket-cdn-01.geobasket.ru/vol2056/part205694/205694185/images/big/1.webp",
        "full_price": 67740000,
        "sell_price": 24830000,
        "title": "Воздуходувка беспроводная"
    },
    {
        "id": 31913050,
        "url": "https://www.wildberries.ru/catalog/31913050/detail.aspx",
        "photo": "https://alm-basket-cdn-01.geobasket.ru/vol319/part31913/31913050/images/big/1.webp",
        "full_price": 306290000,
        "sell_price": 191980000,
        "title": "Бензиновая ранцевая воздуходувка ВР 700"
    }
]

main_data = [wb_data, uzum_data]
service_titles = ["WildBerries", "Uzum Market"]

# @router.message(CommandStart())
# async def start_handler(message: Message):
#     await message.answer("✅ Xush kelibsiz!")
@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Добро пожаловать! \nОтправьте мне изображение, и я найду этот товар на Uzum Market и Wildberries.")

@router.message(F.photo)
async def photo_handler(message: Message, bot: Bot):
    photo = message.photo[-1]
    
    # Download to file
    file = await bot.get_file(photo.file_id)
    
    file_path = file.file_path
    saved_path = f"photos/{photo.file_unique_id}.jpg"

    os.makedirs("photos", exist_ok=True)
    answer = await message.answer("✅ Фото получен!")
    await asyncio.sleep(3)

    await bot.download_file(file_path, saved_path)

    await answer.edit_text("🤖Анализирую фото! Пожалуйста, подождите...")
    await asyncio.sleep(3)
    await answer.edit_text("🔍 Ищу подходящие варианты!")
    for idx, products in enumerate([uzum_data[:3], wb_data[:3]]):
        offset = 0
        limit = 3
        service_title = service_titles[idx]
        await message.answer(f"📦 Найденные товары из <b>{service_title}</b>:", parse_mode=ParseMode.HTML)
        for index, item in enumerate(products):
             # Simulate processing time
            schema = MainItemSchema.model_validate(item)
            show_more_data = None
            button_text = None
            if index == limit - 1:
                show_more_data = {
                    "offset": offset + limit,
                    "service_title": service_title,
                }
                button_text = f"Показать ещё товары из {service_title}"

            markup = build_keyboard(schema.url, show_more_data, button_text)
            caption = generate_caption(service_title, schema)
            await message.answer_photo(photo=schema.photo, caption=caption, reply_markup=markup, parse_mode=ParseMode.HTML)
        await asyncio.sleep(2)



@router.message(F.text)
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
    offset = data.get("offset")
    service_title = data.get("service_title")
    limit = 3
    products = uzum_data[3:] if service_title == "Uzum Market" else wb_data[3:]
    await callback.message.answer(f"📦 Найденные товары из <b>{service_title}</b>:", parse_mode=ParseMode.HTML)

    for index, item in enumerate(products):
        schema = MainItemSchema.model_validate(item)
        show_more_data = None
        button_text = None
        if index == limit - 1:
            show_more_data = {
                "offset": offset + limit,
                "service_title": service_title,
            }
            button_text = f"Показать ещё товары из {service_title}"

        markup = build_keyboard(schema.url, show_more_data, button_text)
        caption = generate_caption(service_title, schema)
        await callback.message.answer_photo(photo=schema.photo, caption=caption, reply_markup=markup, parse_mode=ParseMode.HTML)
# @router.callback_query(F.data)
# async def handle_show_more(callback: CallbackQuery):
#     data = cache.get(callback.data)

#     if not data:
#         markup = callback.message.reply_markup
#         if markup and markup.inline_keyboard:
#             new_keyboard_rows = markup.inline_keyboard[:-1]
#             new_markup = InlineKeyboardMarkup(inline_keyboard=new_keyboard_rows) if new_keyboard_rows else None
#             await callback.message.edit_reply_markup(reply_markup=new_markup)
#         return

#     data = json.loads(data)
#     service = services[data["service_title"]]()
#     search_text = data["text"]
#     main_schema = await service.search(text=search_text, offset=data["offset"])

#     for index, item in enumerate(main_schema.items):
#         show_more_data = None
#         button_text = None
#         if main_schema.offset + main_schema.limit < main_schema.total and index == main_schema.limit - 1:
#             show_more_data = {
#                 "offset": main_schema.offset + main_schema.limit,
#                 "service_title": main_schema.service_title,
#                 "text": search_text
#             }
#             button_text = f"{main_schema.service_title} dagi mahsulotlardan yana ko'rsatish"

#         markup = build_keyboard(item.url, show_more_data, button_text)
#         caption = generate_caption(main_schema.service_title, item)
#         await callback.message.answer_photo(photo=item.photo, caption=caption, reply_markup=markup, parse_mode=ParseMode.HTML)
