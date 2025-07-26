import asyncio
import aiohttp
from services.iswb.schema import ISWBSchema, CategoryDetectionSchema
from services.iswb.cryptographer import Cryptographer
from services.iswb.cropper import Cropper
import aiofiles
from django.core.cache import cache

class ISWBService:
    async def category_detection(self, image_path: str = 'C:/Users/HP/Downloads/app.jpg'):
        url = "https://category-detection.wildberries.ru/api/triton_predict_sync"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
        }
        form_data = aiohttp.FormData()
        async with aiofiles.open(image_path, 'rb') as img_file:
            image_bytes = await img_file.read()
            form_data.add_field('image_file', image_bytes, filename='app.jpg')

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=form_data) as response:
                json = await response.json()
                data = CategoryDetectionSchema.model_validate(json)
                return data

    async def search(self, image_path: str = 'C:/Users/HP/Downloads/app.jpg', offset:int=0, limit:int=3) -> ISWBSchema:
        json = cache.get(image_path)
        url = 'https://rec-filters.wildberries.ru/api/v3/recsAndFilters/imageSearch'
        cryptographer = Cryptographer()
        cropper = Cropper()
        encrypted_headers = cryptographer.generate_encrypted_headers()
        headers = {
            'deviceId': '6fbf083f0e66e8da',
            'devicename': 'Android, V2266A(V2266A)',
            'devicetoken': 'd_NrmfGRSoapMEJkhDMh1v:APA91bHk_gQy8vwFTEItsILABKeGWvzS4kMNhp8SsQ_rbTvFgTtecfVtPyiVW-9iLeOnPFt-veT-YAVxv9VkmD3DX3tKk18SmS1qFFONvD8VM220OLkodK8',
            'RequestUUID': encrypted_headers.get('uuid'),
            'Signature': encrypted_headers.get('encodedUuid'),
            'Site-Locale': 'uz',
            'X-ClientInfo': 'hide_dtype=10;14;13;dest=494;lang=uz;curr=uzs;spp=30;locale=uz;appType=32',
            'X-Pow': '1|8|1750439105|709a0c88-3db3-4276-a15f-ee7e6945c60d|MjQ4|'
        }

        category_detection_schema = await self.category_detection(image_path=image_path)
        predictions = category_detection_schema.predictions
        for prediction in predictions:
            params = {
                "label_list": prediction.label,
            }
            cropped_path = cropper.crop_image(image_path, prediction.bbox)
            form_data = aiohttp.FormData()
            async with aiofiles.open(cropped_path, 'rb') as img_file:
                image_bytes = await img_file.read()
                form_data.add_field('image', image_bytes)

            async with aiohttp.ClientSession() as session:
                async with session.post(url, params=params, headers=headers, data=form_data) as response:
                    response.raise_for_status()
                    json = await response.json()
                    data = ISWBSchema.model_validate(json)
                    cache.set(image_path, data.model_dump_json(), timeout=86400)
                    return data.to_main_schema(offset=offset, limit=limit)
                


