from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Dict, Any, Callable, Awaitable
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types.base import TelegramObject
from apscheduler_di import ContextSchedulerDecorator

class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: ContextSchedulerDecorator):
        super().__init__()
        self.scheduler = scheduler

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data['apscheduler'] = self.scheduler
        return await handler(event, data)