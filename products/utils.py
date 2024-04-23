import environ
import asyncio
from aiogram import Bot

env = environ.Env()
environ.Env.read_env(env_file=".env")


BOT_TOKEN = env('TG_BOT_TOKEN')
OPERATORS = env('OPERATORS_CHAT_ID').split(',')

async def send_new_review(message):
    bot = Bot(BOT_TOKEN)
    for chat_id in OPERATORS:
        await bot.send_message(chat_id=chat_id, text=message)

async def main():
    await send_new_review('Здравствуйте!')

if __name__ == '__main__':
    asyncio.run(main())
