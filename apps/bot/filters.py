from aiogram.filters import Filter
from django.core.cache import cache

class PhotoCallbackFilter(Filter):
    def __init__(self):
        self.data = "photo_"

    async def __call__(self, callback_query):
        return callback_query.data and callback_query.data.startswith(self.data)


class TextCallbackFilter(Filter):
    def __init__(self):
        self.data = "text_"

    async def __call__(self, callback_query):
        return callback_query.data and callback_query.data.startswith(self.data)

class RemoveButtonCallbackFilter(Filter):
    def __init__(self):
        pass

    async def __call__(self, callback_query):
        return callback_query.data and not cache.get(callback_query.data)