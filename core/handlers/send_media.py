from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.types import Message, FSInputFile, InputMediaPhoto, InputMediaVideo
from aiogram import Bot
from aiogram.utils.chat_action import ChatActionSender


async def get_audio(message: Message, bot: Bot):
    async with ChatActionSender.typing(chat_id=message.chat.id, bot=bot):
        audio = FSInputFile(path=r'files\AudioFile.mp3', filename='AudioFile.mp3')
        await bot.send_audio(message.chat.id, audio=audio)


async def get_document(message: Message, bot: Bot):
    document = FSInputFile(path=r'C:\Users\Administrator\Desktop\photo\document.docx')
    await bot.send_document(message.chat.id, document=document, caption='Its document')


async def get_media_group(message: Message, bot: Bot):
    photo1_mg = InputMediaPhoto(type='photo', media=FSInputFile(r'C:\Users\Administrator\Desktop\photo\image.jpg'),
                                caption='Its mediagroup')
    photo2_mg = InputMediaPhoto(type='photo', media=FSInputFile(r'C:\Users\Administrator\Desktop\photo\sticker.png'))
    video_mg = InputMediaVideo(type='video', media=FSInputFile(r'C:\Users\Administrator\Desktop\photo\Robots_video.mp4'))
    media = [photo2_mg, photo1_mg, video_mg]
    await bot.send_media_group(message.chat.id, media)


async def get_photo(message: Message, bot: Bot):
    photo = FSInputFile(r'C:\Users\Administrator\Desktop\photo\image.jpg')
    await bot.send_photo(message.chat.id, photo, caption='Its photo')


async def get_sticker(message: Message, bot: Bot):
    sticker = FSInputFile(r"C:\Users\Administrator\Desktop\photo\sticker.png")
    await bot.send_sticker(message.chat.id, sticker)


async def get_video(message: Message, bot: Bot):
    video = FSInputFile(r"C:\Users\Administrator\Desktop\photo\Robots_video.mp4")
    await bot.send_video(message.chat.id, video)


async def get_video_note(message: Message, bot: Bot):
    video_note = FSInputFile(r"C:\Users\Administrator\Desktop\photo\Robots_video_note.mp4")
    await bot.send_video_note(message.chat.id, video_note)


async def get_voice(message: Message, bot: Bot):
    voice = FSInputFile(r"C:\Users\Administrator\Desktop\photo\voice.opus")
    await bot.send_voice(message.chat.id, voice)