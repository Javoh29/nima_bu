from django.core.management.base import BaseCommand

from services.olx.service import OlxService
from services.uzum.service import UzumService
from services.main.service import MainService


class Command(BaseCommand):
    help = 'This is a simple custom command'

    def handle(self, *args, **kwargs):
        async def run():
            async for task in MainService().search("sichqoncha"):
                print(task)
        import asyncio

        asyncio.run(run())

        # asyncio.run(UzumService().search("pc"))