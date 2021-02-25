from aiogram import Bot, Dispatcher, executor, types
import requests
from bs4 import BeautifulSoup as bs
import aiogram
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

button1 = types.InlineKeyboardButton('Курс', callback_data='price')
button2 = types.InlineKeyboardButton('Баланс', callback_data='balance')
markup1 = InlineKeyboardMarkup(resize_keyboard=True).row(button1, button2)

bot = Bot(token='1053546310:AAHPrGDeGr-aBcZXsZZO8SZNbTb87W-1RWY')
dp = Dispatcher(bot)
url = 'https://www.coingecko.com/ru/Криптовалюты/marlin'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.396'}


def getPrice():
    html = requests.get(url, headers=HEADERS)
    soup = bs(html.text, 'html.parser')
    output = soup.find('span', class_='no-wrap')
    a = list(output)
    c = ''.join(a[0:134])
    return c


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Привет!", reply_markup=markup1)


@dp.callback_query_handler(lambda c: c.data == 'price')
async def process_getPrice(message: types.Message):
    await bot.send_message(message.from_user.id, 'Текущий курс: ' + getPrice(), reply_markup=markup1)


@dp.callback_query_handler(lambda c: c.data == 'balance')
async def process_getPrice(message: types.Message):
    d = list(getPrice())
    e = d[3:1000]
    f = d[2]
    if f == '0':
        currentBalance = round((int(''.join(e)) / 100000) * 626.25987020, 2)
        await bot.send_message(message.from_user.id, 'Ваш баланс: ' + str(currentBalance) + '$', reply_markup=markup1)
    else:
        try:
            if d[14] == '0' and  d[15] == '0' and d[16] == '0' and d[17] == '0' and d[18] == '0':
                currentBalance = round((int(''.join(e)) / 100000) * 626.25987020, 2)
            else:
                currentBalance = round((int(''.join(d[3:10])) / 1000000) * 626.25987020, 3) 
        except IndexError:
                 currentBalance = round((int(''.join(d[3:10])) / 1000000) * 626.25987020, 2) 
        await bot.send_message(message.from_user.id, 'Ваш баланс: ' + str(currentBalance) + '$', reply_markup=markup1)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
