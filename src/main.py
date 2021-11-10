import os
import logging
import telebot
from telebot import types
from pprint import pprint

from dotenv import load_dotenv

from minio_client import MinioHandler

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
BOT_NAME = os.getenv('BOT_NAME')
MINIO_ACCESS = os.getenv('ACCESS_KEY')
MINIO_SECRET = os.getenv('SECRET_KEY')

bot = telebot.TeleBot(TOKEN)


class Picture:
    def __init__(self):
        self.picture = 0
        self.text = ''


@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    picture_button = types.InlineKeyboardButton(text='Add text', callback_data='text')
    gif_button = types.InlineKeyboardButton(text='Create gif', callback_data='gif')
    keyboard.add(picture_button, gif_button)
    bot.send_message(
        message.chat.id,
        f'Hello, {message.from_user.first_name}!\n' +
        'I\'m here to help you to add your text to your picture\n' +
        'or to create your own gif picture! \n' +
        'To add your text to the picture press "Add text"\n' +
        'To create gif press "Create gif"',
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: True)
def choose_option(call):
    if call.data == 'text':
        bot.send_message(
            call.message.chat.id,
            'Ok! Enter the text you want to add'
        )
        bot.register_next_step_handler(call.message, wait_for_text)
    elif call.data == 'gif':
        bot.send_message(
            call.message.chat.id,
            'Add three or more pictures '
        )
        bot.register_next_step_handler(call.message, create_gif)


@bot.message_handler(content_types=['text'])
def wait_for_text(message):
    try:
        text = str(message.text)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        lobster_button = types.InlineKeyboardButton(text='lobster', callback_data='lobster')
        comfortaa_button = types.InlineKeyboardButton(text='comfortaa', callback_data='comfortaa')
        keyboard.add(lobster_button, comfortaa_button)
        bot.send_message(
            message.from_user.id,
            'Now it\'s time to choose the font you like ',
            reply_markup=keyboard
        )
    except TypeError:
        bot.send_message(
            message.from_user.id,
            'Please enter correct text'
        )


def choose_font(message):
    if message.text == 'Lobster':
        font = 'Lobster'
    elif message.text == 'Comfortaa':
        font = 'Comfortaa'
    bot.send_message(
        message.from_user.id,
        f'And now, add picture you want '
    )
    bot.register_next_step_handler(message, create_picture)


def create_picture(message):
    try:
        if message.content_type == 'photo':
            picture = message.photo[-1].file_id
            bot.send_message(
                message.from_user.id,
                'Please, wait...'
            )
            bot.send_photo(
                message.from_user.id,
                picture
            )
    except TypeError:
        bot.send_message(
            message.from_user.id,
            'Please add correct image'
        )


def create_gif(message):
    try:
        if message.content_type == 'photo':
            pass
    except TypeError:
        pass


if __name__ == '__main__':
    bot.infinity_polling()






# class LongPolling:
#     def __init__(self, bot_name, token):
#         self.bot_name = bot_name
#         self.token = token
#         self.response = url + self.bot_name + self.token + '/getUpdates'
#         self.get_updates()
#
#     def get_updates(self):
#         while True:
#             time.sleep(1)
#             return http.request('GET', self.response)
