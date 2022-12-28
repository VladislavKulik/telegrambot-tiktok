import re
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputTextMessageContent, InlineQueryResultArticle

API_TOKEN = '5957238015:AAHpPAIqxW5PePj0IkMeDx2gfCOky82yhkc'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    name = State()

class download(StatesGroup):
    name = State()

headers = {
    'Accept-language': 'en',
    'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) '
                  'Version/4.0.4 Mobile/7B334b Safari/531.21.102011-10-16 20:23:10'
}

def download_video(url):
    request_url = f'https://api.douyin.wtf/api?url={url}'
    response = requests.get(request_url, headers=headers)
    video_link = response.json()['video_data']['nwm_video_url_HQ']
    return video_link

def download_photo(url):
    request_url = f'https://api.douyin.wtf/api?url={url}'
    response = requests.get(request_url, headers=headers)
    photo_link = response.json()['video_data']['no_watermark_image_list']
    return photo_link


# @dp.message_handler(commands=['start', 'help'])
# async def send_welcome(message: types.Message):
#     await message.reply(f'Selamat datang, {message.chat.first_name}!\n\nAnda dapat memulai dengan klik /download atau /list \n'
#                         f'Maka video anda akan saya Download!\n\nSaat ini, saya mendukung '
#                         f'hanya video dari TikTok!')
#     btn1 = InlineKeyboardButton('/download', '/download')
#     btn2 = InlineKeyboardButton('/list', '/list')
#     markup4 = ReplyKeyboardMarkup(resize_keyboard=True).row(
#         btn1, btn2
#     )
#     await message.answer('Pilih',reply_markup=markup4)

# @dp.message_handler(commands=['list', 'List'])
# async def send_list(message: types.Message, state: FSMContext):
#     await Form.name.set()
#     await message.reply(f'📚 Kirim List Video Tiktok :\n'
#                         f'Pisahkan setiap link video dengan ↩')

# @dp.message_handler(state=Form.name)
# async def process_name(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.reply(f"Hello, {message.chat.first_name}!\nMohon tunggu sebentar 😊")
#     video_list = message.text.split('\n')
#     counter = 0
#     while counter < len(video_list):
#         video_link = download_video(video_list[counter])
#         await message.reply_video(video_link, caption='Saya senang bisa membantu! Salam, @unduhtiktokbot')
#         counter = counter + 1
#     else:
#         print('Done')

@dp.message_handler(commands=['start', 'Start'])
async def send_video(message: types.Message):
    await download.name.set()
    await message.reply(f'Бот работает, скиньте ссылку на ТикТок')


@dp.message_handler(state=download.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.finish()
    if re.compile('https://[a-zA-Z]+.tiktok.com/').match(message.text):
        video_link = download_video(message.text)
        caption = hlink("Ссылка", message.text), hlink(message.from_user.username, "tg://user?id="+str(message.from_user.id)+"")
        await message.reply_video(video_link, caption=caption, parse_mode=ParseMode.HTML)
        await message.delete()
        return await download.name.set()
    if re.compile('https://[a-zA-Z]+.tiktok.com/').match(message.text):
        photo_link = download_photo(message.text)
        caption = hlink("Ссылка", message.text), hlink(message.from_user.username, "tg://user?id="+str(message.from_user.id)+"")
        await message.reply_photo(photo_link, caption=caption, parse_mode=ParseMode.HTML)
        await message.delete()
        return await download.name.set()
    else:
        await message.answer('⛔️ Anda mengirim tautan yang tidak didukung oleh bot!\nKetik /help untuk bantuan')
    

# @dp.inline_handler()
# async def inline_handler(querry: types.InlineQuery):
#     Text = querry.query or "echo"
#     Link
#     await querry.answer(art) 
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)