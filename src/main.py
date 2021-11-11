import os
import logging
import telebot
from telebot import types
from pprint import pprint
from pil_handler import PictureWithText

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
            'Add more than three pictures '
        )
        bot.register_next_step_handler(call.message, create_gif)


@bot.message_handler(content_types=['text'])
def wait_for_text(message):
    try:
        text = str(message.text)
        # keyboard = types.ReplyKeyboardMarkup(row_width=2)
        # lobster_button = types.KeyboardButton(text='lobster')
        # comfortaa_button = types.KeyboardButton(text='comfortaa')
        # keyboard.add(lobster_button, comfortaa_button)
        # bot.send_message(
        #     message.from_user.id,
        #     'Now it\'s time to choose the font you like ',
        #     reply_markup=keyboard
        # )
        bot.send_message(
            message.from_user.id,
            f'And now, add picture you want '
        )
        bot.register_next_step_handler(message, create_picture, text)
    except TypeError:
        bot.send_message(
            message.from_user.id,
            'Please enter correct text'
        )


def create_picture(message, text: str):
    try:
        if message.content_type == 'photo':
            picture_info = bot.get_file(message.photo[-1].file_id)
            bot.send_message(
                message.from_user.id,
                f'Please, wait...'
            )
            picture_file = bot.download_file(picture_info.file_path)
            print(type(picture_file))
            changed_picture = PictureWithText(picture_file, text)
            bot.send_photo(
                message.from_user.id,
                changed_picture
            )
    except TypeError:
        bot.send_message(
            message.from_user.id,
            'Please add correct image'
        )
        bot.register_next_step_handler(message, create_picture, text)


def create_gif(message):
    try:
        if message.content_type == 'photo':
            pass
    except TypeError:
        pass


if __name__ == '__main__':
    bot.infinity_polling()
