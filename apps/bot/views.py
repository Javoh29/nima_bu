from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from aiogram.types import Update
from .main import dp, bot
import json
import asyncio

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        try:
            update = Update.model_validate_json(request.body.decode('utf-8'))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

        asyncio.get_event_loop().create_task(dp.feed_update(bot, update))
        return JsonResponse({"ok": True})
    return JsonResponse({"error": "Invalid method"}, status=405)
