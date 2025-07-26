from django.core.management.base import BaseCommand
import asyncio



class Command(BaseCommand):
    help = 'This is a simple custom command'

    def handle(self, *args, **kwargs):
        async def run():
            from services.iswb.service import ISWBService
            service = ISWBService()
            data = await service.search()
            print(data)
            


        asyncio.run(run())




        # asyncio.run(run())

        # asyncio.run(UzumService().search("pc"))