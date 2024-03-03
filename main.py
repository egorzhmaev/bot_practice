import asyncio
import logging
import asyncpg
from datetime import datetime, timedelta


from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender

from core.handlers.basic import get_start, get_photo, get_hello, get_location, get_inline
from core.handlers.contact import get_fake_contact, get_true_contact
from core.handlers import apsched
from core.handlers.callback import select_macbook
from core.handlers import form
from core.handlers.pay import order, pre_checkout_query, success_payment, shipping_check
from core.handlers import send_media

from core.settings import settings

from core.filtres.iscontact import IsTrueContact

from core.middleware.countermiddleware import CounterMiddleware
from core.middleware.officehours import OfficeHoursMiddleware
from core.middleware.dbmiddleware import DbSession
from core.middleware.apschedulermiddleware import SchedulerMiddleware
from core.middleware.example_chat_action_middleware import ExampleChatActionMiddleware

from core.utils.callbackdata import MacInfo
from core.utils.statesform import StepsForm
from core.utils.commands import set_commands

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler_di import ContextSchedulerDecorator


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен!')
async def close_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот закрыт!')


async def start():

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                                "(%(filename)s).%(funcName)s(%(lineno)d)) - %(message)s")

    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')

    pool_connect = await asyncpg.create_pool(user="postgres", password="postgres", database="user",
                                             host="127.0.0.1", port=5432, command_timeout=60)

    storage = RedisStorage.from_url('redis://localhost:6379/0')
    dp = Dispatcher(storage=storage)
    jobstores = {
        'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
                                 run_times_key='dispatched_trips_running',
                                 host='localhost',
                                 db=2,
                                 port=6379)
    }

    scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone="Asia/Yekaterinburg", jobstores=jobstores))
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    scheduler.add_job(apsched.send_message_time, trigger='date', run_date=datetime.now() + timedelta(seconds=10))
    scheduler.add_job(apsched.send_message_cron, trigger='cron', hour=datetime.now().hour,
                      minute=datetime.now().minute + 1, start_date=datetime.now())
    scheduler.add_job(apsched.send_message_interval, trigger='interval', seconds=60)
    scheduler.remove_all_jobs()
    scheduler.start()

    dp.update.middleware.register(DbSession(pool_connect))
    dp.update.middleware.register(OfficeHoursMiddleware())
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    dp.message.middleware.register(CounterMiddleware())
    dp.message.middleware.register(ExampleChatActionMiddleware())
    dp.startup.register(start_bot)
    dp.shutdown.register(close_bot)

    dp.message.register(send_media.get_audio, Command(commands='audio'))
    dp.message.register(send_media.get_document, Command(commands='document'), flags={'chat_action': 'upload_document'})
    dp.message.register(send_media.get_media_group, Command(commands='mediagroup'), flags={'chat_action': 'upload_photo'})
    dp.message.register(send_media.get_photo, Command(commands='photo'), flags={'chat_action': 'upload_photo'})
    dp.message.register(send_media.get_sticker, Command(commands='sticker'), flags={'chat_action': 'choose_sticker'})
    dp.message.register(send_media.get_video, Command(commands='video'), flags={'chat_action': 'upload_video'})
    dp.message.register(send_media.get_video_note, Command(commands='video_note'), flags={'chat_action': 'upload_video_note'})
    dp.message.register(send_media.get_voice, Command(commands='voice'), flags={'chat_action': 'upload_voice'})


    dp.message.register(order, Command(commands=['pay']))
    dp.message.register(form.get_form, Command(commands='form'))
    dp.message.register(form.get_name, StepsForm.GET_NAME)
    dp.message.register(form.get_last_name, StepsForm.GET_LAST_NAME)
    dp.message.register(form.get_age, StepsForm.GET_AGE)

    dp.shipping_query.register(shipping_check)
    dp.pre_checkout_query.register(pre_checkout_query)
    dp.callback_query.register(select_macbook, MacInfo.filter())

    dp.message.register(form.get_form, Command(commands="form"))
    dp.message.register(success_payment, F.successful_payment)
    dp.message.register(get_location, F.location)
    dp.message.register(get_photo, F.photo)
    dp.message.register(get_true_contact, F.contact, IsTrueContact())
    dp.message.register(get_fake_contact, F.contact)
    dp.message.register(get_hello, F.text == 'Привет')
    dp.message.register(get_inline, Command(commands=['inline']))
    dp.message.register(get_start, Command(commands=['start']))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())

