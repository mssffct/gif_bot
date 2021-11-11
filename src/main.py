import os
import logging
import telebot
from telebot import types
from pprint import pprint
from pil_handler import PictureWithText, GifPicture

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
        'I\'m here to help you with adding your text to your picture\n' +
        'or creating your own gif picture! \n' +
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
        frames = []
        bot.send_message(
            call.message.chat.id,
            'Add more than three pictures '
        )
        bot.register_next_step_handler(call.message, create_gif, frames)


@bot.message_handler(content_types=['text'])
def wait_for_text(message):
    try:
        text = str(message.text)
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        lobster_button = types.KeyboardButton(text='Lobster')
        comfortaa_button = types.KeyboardButton(text='Comfortaa')
        keyboard.add(lobster_button, comfortaa_button)
        bot.send_message(
            message.chat.id,
            'Ok! It\'s time to choose the font you like ',
            reply_markup=keyboard
        )
        bot.register_next_step_handler(message, choose_font, text)
    except TypeError:
        bot.send_message(
            message.from_user.id,
            'Please enter correct text'
        )
        bot.register_next_step_handler(message, wait_for_text)


def choose_font(message, text):
    font = ''
    if message.text == 'Lobster':
        font = 'Lobster-Regular.ttf'
    elif message.text == 'Comfortaa':
        font = 'Comfortaa-Medium.ttf'
    bot.send_message(
        message.from_user.id,
        f'And now, add picture you want ',
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(message, create_picture, text, font)


def create_picture(message, text: str, font: str):
    try:
        if message.content_type == 'photo':
            picture_info = bot.get_file(message.photo[-1].file_id)
            bot.send_message(
                message.from_user.id,
                f'Please, wait...'
            )
            picture_file = bot.download_file(picture_info.file_path)
            changed_picture = PictureWithText(picture_file, text, font).changed
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


def create_gif(message, frames: list):
    print("func called")
    pprint(vars(message))
    try:
        if message.content_type == 'photo':
            pass

    except TypeError:
        pass
    print(frames)

@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    return downloaded_file


if __name__ == '__main__':
    bot.infinity_polling()
