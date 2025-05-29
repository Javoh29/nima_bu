from services.base import BaseService
from services.olx.service import OlxService
from services.uzum.service import UzumService
import asyncio
from typing import AsyncGenerator
from services.main.schema import MainSchema

class MainService:
    service_list: list[BaseService] = [UzumService, OlxService]
    async def search(self, text: str, offset: int = 0, limit: int = 3) -> AsyncGenerator[MainSchema, None]:
        tasks = set()
        for service in self.service_list:
            tasks.add(asyncio.create_task(service().search(text=text, offset=offset, limit=limit)))
        while tasks:
            done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for finished in done:
                result = finished.result()
                yield result