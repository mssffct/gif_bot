import os

import pytest
import telebot
from dotenv import load_dotenv
from telebot import types

from src.main import get_gifs_command, help_command, start_command

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')


def test_commands_handlers():
    bot = telebot.TeleBot(TOKEN)
    help_command, description, lang = 'help', 'start', 'en'
    scope = telebot.types.BotCommandScopeChat('752272448')
    ret_msg = bot.set_my_commands([telebot.types.BotCommand(help_command, description)], scope, lang)
    assert ret_msg is True