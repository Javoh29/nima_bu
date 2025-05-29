from django.core.management.base import BaseCommand
from apps.bot.main import main
import asyncio

class Command(BaseCommand):
    help = 'This is a simple custom command'

    def handle(self, *args, **kwargs):
        asyncio.run(main())

        # asyncio.run(UzumService().search("pc"))