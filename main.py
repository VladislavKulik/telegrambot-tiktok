import re
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode

API_TOKEN = '5957238015:AAHpPAIqxW5PePj0IkMeDx2gfCOky82yhkc'
# API_TOKEN = '5936321734:AAGhSAa2QgupRPjPgX2j38pol2jBjofejOo'
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


def download_media(url):
    request_url = f'https://api.douyin.wtf/api?url={url}'
    response = requests.get(request_url, headers=headers)
    video_link = response.json()['video_data']['nwm_video_url_HQ']
    return video_link


@dp.message_handler(commands=['start', 'Start'])
async def send_welcome(message: types.Message):
    await download.name.set()
    await message.reply(f'Бот работает, скиньте ссылку на ТикТок')


@dp.message_handler(commands=['help', 'Help'])
async def send_help(message: types.Message):
    await download.name.set()
    await message.reply(f'Бог поможет')


@dp.message_handler(commands=['rules', 'Rules'])
async def send_rules(message: types.Message):
    await download.name.set()
    await message.reply(f'Правила бота: \n' f'1. Без алкоголя\n' f'2. Без оскорблений\n' f'3. Без доты\n' f'4. Адекватность приветствуется')


@dp.message_handler(commands=['analyzer', 'Analyzer'])
async def send_rules(message: types.Message):
    await download.name.set()
    await message.reply(f'Сентимент: негативний \n' f'Кількість позитивних слів: 0 \n' f'Кількість негативних слів: 2\n'f'Кількість нейтральних слів: 4\n'f'Кількість загальних слів: 9\n')


# @dp.message_handler(state=download.name)
# async def process_name(message: types.Message, state: FSMContext):
#     await state.finish()
#     if re.compile('https://[a-zA-Z]+.tiktok.com/').match(message.text):
#         link = download_media(message.text)
#         caption = hlink("Ссылка", message.text), hlink(
#             message.from_user.username, "tg://user?id="+str(message.from_user.id)+"")
#         await message.reply_video(link, caption=caption, parse_mode=ParseMode.HTML)
#         await message.delete()
#         return await download.name.set()
#     else:
#         await message.answer('Походу Бот сломался (может и нет). Почему он сломался, я не знаю.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
