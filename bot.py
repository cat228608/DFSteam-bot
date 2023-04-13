import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
import requests

token = "5940917891:AAF0Op" #Токен от бота

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.answer("[ANTIFLOOD] - STOP! FUCK STOP!")
    
@dp.message_handler(commands="start")
@dp.throttled(anti_flood,rate=3)
async def start(message: types.Message):
    await bot.send_message(message.chat.id, "<b>Добро Пожаловать в бота DFSteam!</b>\n\nПросто отправь мне ссылку на мод с мастерской стим\nИ я попробую его скачать для тебя.", parse_mode="HTML")
    
@dp.message_handler(content_types=["text"]) 
@dp.throttled(anti_flood,rate=3)
async def get_site(message: types.Message):
    steam_site = message.text
    if "https://steamcommunity.com/sharedfiles/filedetails/?id" in steam_site:
        headers = {
        'authority': 'api.ggntw.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'access-token': '',
        'content-type': 'application/json',
        'origin': 'https://ggntw.com',
        'referer': 'https://ggntw.com/',
        'sec-ch-ua': '"Not?A_Brand";v="99", "Opera";v="97", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36 OPR/48.0.2685.52',
        }
        json_data = {
            'url': steam_site,
        }
        
        try:
            response = requests.post('https://api.ggntw.com/steam.request', headers=headers, json=json_data) #Аня я люблю тебя
            pars = response.json()
            image = pars['image']
            name = pars['name']
            size = pars['size']
            update = pars['update']
            url = pars['url']
            urlkb = types.InlineKeyboardMarkup(row_width=1)
            urlButton = types.InlineKeyboardButton('Скачать мод', url=f'{url}')
            urlkb.add(urlButton)
            await bot.send_photo(message.chat.id, image, caption=f'<b>Название:</b> {name}\n<b>Последнее обновление:</b> {update}\n<b>Размер мода:</b> {size}', parse_mode="HTML", reply_markup=urlkb)
        except Exception as er:
            print(er)
    else:
        await bot.send_message(message.chat.id, "Некорректная ссылка!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)