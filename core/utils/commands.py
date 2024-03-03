from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command = 'start',
            description = 'Начало работы'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        ),
        BotCommand(
            command='cancel',
            description='Сбросить'
        ),
        BotCommand(
            command='inline',
            description='Кдавиатура Инлайн'
        ),
        BotCommand(
            command='pay',
            description='Купить продукт'
        ),
        BotCommand(
            command='from',
            description='Начать опрос'
        ),
        BotCommand(
            command='audio',
            description='Отправить музыку'
        ),
        BotCommand(
            command='document',
            description='Отправить документ'
        ),
        BotCommand(
            command='mediagroup',
            description='Прислать медиагруппу'
        ),
        BotCommand(
            command='photo',
            description='Прислать фото'
        ),
        BotCommand(
            command='sticker',
            description='Отправить стикер'
        ),
        BotCommand(
            command='video',
            description='Отправить видео'
        ),
        BotCommand(
            command='video_note',
            description='Прислать видео-сообщение'
        ),
        BotCommand(
            command='voice',
            description='Прислать голосовое сообщение'
        )

    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())