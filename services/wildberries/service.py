import asyncio
import aiohttp
from services.base import BaseService
from services.olx.schema import OlxSearchSchema
from services.wildberries.schema import WildberriesSearchSchema
import json


class WildberriesService(BaseService):

    async def search(self, text: str, offset: int = 0, limit: int = 3) -> dict:
        url = "https://search.wb.ru/exactmatch/sng/common/v11/search"


        params = {
            "ab_testid": "price_01_03",
            "appType": "32",
            "curr": "uzs",
            "dest": "494",
            "hide_dtype": "10%3B14%3B13",
            "lang": "uz",
            "locale": "uz",
            "page": offset//30+1,   
            "query": text,
            "resultset": "catalog",
            "sort": "popular",
            "spp": limit,
            "suppressSpellcheck": "false",

        }
        headers = {
            'Site-Locale': 'uz',
            'Accept-Encoding': 'application/json',
            'Content-Type': 'application/json',
            'WB-AppLanguage': 'uz'
        }



        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                try:
                    text = await response.text()
                    schema = WildberriesSearchSchema.model_validate_json(text)
                    return schema.to_main_schema(offset=offset, limit=limit)
                except Exception as e:
                    print(e)
                    return

