import os
import time

import telebot
from dotenv import load_dotenv
from telebot import types

from keyboards import font_keyboard, main_keyboard
from minio_client import MinioHandler
from pil_handler import GifPicture, PictureWithText

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
MINIO_ACCESS = os.getenv('MINIO_ROOT_USER')
MINIO_SECRET = os.getenv('MINIO_ROOT_PASSWORD')
temp_path = os.path.join('..', 'temp')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        f'Hello, {message.from_user.first_name}!\n' +
        'I\'m here to help you with adding your text to your picture\n' +
        'or creating your own gif picture! \n' +
        'To add your text to the picture press "Add text"\n' +
        'To create gif press "Create gif"',
        reply_markup=main_keyboard
    )


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        f'Hello, {message.from_user.first_name}!\n' +
        'I\'m here to help you with adding your text to your picture\n' +
        'or creating your own gif picture! \n' +
        'To start, press or type in command /start \n' +
        'To add your text to the picture press "Add text"\n' +
        'To create gif press "Create gif" \n' +
        'Then simply follow the instructions. \n' +
        'To get your gifs use command /get_gifs \n'
    )


@bot.message_handler(commands=['get_gifs'])
def get_gifs_command(message):
    global temp_path
    uid = message.from_user.id
    minio.get_gifs(uid)
    for gif in os.listdir(temp_path):
        io_file = open(f'{temp_path}\\{gif}', 'rb')
        bot.send_document(
            message.from_user.id,
            io_file
        )
        io_file.close()
    temp_clean()


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
        bot.register_next_step_handler(call.message, send_gif)


@bot.message_handler(content_types=['text'])
def wait_for_text(message):
    if message.content_type == 'text':
        text = str(message.text)
        bot.send_message(
            message.chat.id,
            'Ok! It\'s time to choose the font you like ',
            reply_markup=font_keyboard
        )
        bot.register_next_step_handler(message, choose_font, text)
    else:
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
        'And now, add picture you want ',
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(message, create_picture, text, font)


def create_picture(message, text: str, font: str):
    global temp_path
    try:
        if message.media_group_id is None and message.content_type == 'photo':
            picture_info = bot.get_file(message.photo[-1].file_id)
            path = f'{temp_path}\\{picture_info.file_unique_id}.jpg'
            picture_file = bot.download_file(picture_info.file_path)
            with open(path, 'wb') as new_file:
                new_file.write(picture_file)
            PictureWithText(f'{picture_info.file_unique_id}', text, font)
            photo = open(path, 'rb')
            bot.send_photo(
                message.from_user.id,
                photo
            )
            photo.close()
            minio.save(
                uid=message.from_user.id,
                obj_name=f'{picture_info.file_unique_id}',
                pic_format='jpg'
            )
            os.remove(f'{temp_path}\\{picture_info.file_unique_id}.jpg')
    except TypeError:
        bot.send_message(
            message.from_user.id,
            'Please add correct image'
        )
        bot.register_next_step_handler(message, create_picture, text, font)


@bot.message_handler(content_types=['photo'])
def create_gif(message):
    global temp_path
    try:
        if message.media_group_id is not None:
            picture_info = bot.get_file(message.photo[-1].file_id)
            path = f'{temp_path}\\{picture_info.file_unique_id}.jpg'
            picture_file = bot.download_file(picture_info.file_path)
            with open(path, 'wb') as new_file:
                new_file.write(picture_file)
            GifPicture(message.media_group_id, message.from_user.id)
        else:
            bot.send_message(
                message.from_user.id,
                'Please add two or more pictures'
            )
            bot.register_next_step_handler(message, create_gif)
    except TypeError:
        pass


def send_gif(message):
    global temp_path
    time.sleep(10)
    try:
        file = f'{message.from_user.id}_{message.media_group_id}'
        io_file = open(f'{temp_path}\\{file}.gif', 'rb')
        bot.send_document(
            message.from_user.id,
            io_file
        )
        io_file.close()
        minio.save(
            uid=message.from_user.id,
            obj_name=file,
            pic_format='gif'
        )
        temp_clean()
    except FileNotFoundError:
        bot.register_next_step_handler(message, send_gif)


def temp_clean():
    global temp_path
    for file in os.listdir(temp_path):
        file_path = os.path.join(temp_path, file)
        os.remove(file_path)


if __name__ == '__main__':
    minio = MinioHandler(MINIO_ACCESS, MINIO_SECRET)
    bot.infinity_polling(timeout=10)
