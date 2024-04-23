import environ
import asyncio
from django import forms
from aiogram import Bot, types

from .models import Review

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

from django.forms import Widget
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

class ArrayEditorWidget(Widget):
    def render(self, name, value, attrs=None, renderer=None):
        context = {
            'widget': {
                'name': name,
                'value': value or '[]', 
                'attrs': attrs,
            }
        }
        return mark_safe(render_to_string('search/indexes/products/array_editor_widget.html', context))



if __name__ == '__main__':
    asyncio.run(main())
