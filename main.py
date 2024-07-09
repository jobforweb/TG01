import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

@dp.message(CommandStart())
async def start(message: Message):
  await message.answer("Бот для просмотра погоды. Бот на aiogram.")

@dp.message(Command('help'))
async def help(message: Message):
  await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/weather")

@dp.message(Command('weather'))
async def get_weather(message: Message):
    city = 'Vladivostok'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric'
    response = requests.get(url)
    weather_data = response.json()
    if weather_data['cod'] == 200:
        weather_description = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        await message.reply(f"Погода в городе {city}: {weather_description}. Температура: {temp}°C")
    else:
        await message.reply("Извините, не удалось получить информацию о погоде.")

async def main():
  await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())