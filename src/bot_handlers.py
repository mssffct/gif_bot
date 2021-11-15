import configparser
import os
import telebot

from dotenv import load_dotenv

from minio_client import MinioHandler
from pil_handler import GifPicture, PictureWithText

load_dotenv()
MINIO_ROOT_USER = os.getenv('MINIO_ROOT_USER')
MINIO_ROOT_PASSWORD = os.getenv('MINIO_ROOT_PASSWORD')
HOST_PORT = os.getenv('HOST_PORT')
TOKEN = os.getenv('TELEGRAM_TOKEN')
config = configparser.ConfigParser()
config.read('../config.ini')
temp_path = config['Path']['temp_path']

bot = telebot.TeleBot(TOKEN)

minio = MinioHandler(HOST_PORT, MINIO_ROOT_USER, MINIO_ROOT_PASSWORD)


def get_gifs_command_handler(message):
    """
    Gets all created by {uid} gifs from minio storage
    :param message: tg response message
    :return:
    """
    uid = message.from_user.id
    minio.get_gifs(uid)
    for gif in os.listdir(temp_path):
        io_file = open(f'{temp_path}/{gif}', 'rb')
        bot.send_document(
            message.from_user.id,
            io_file
        )
        io_file.close()
    temp_clean()


def text_to_picture_handler(message, text: str, font: str):
    """
    Places text on a user-submitted image,
    then saves it to minio storage
    :param message: tg response message
    :param text: users text
    :param font: user-selected font
    :return:
    """
    picture_info = bot.get_file(message.photo[-1].file_id)
    path = f'{temp_path}/{picture_info.file_unique_id}.jpg'
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
    os.remove(f'{temp_path}/{picture_info.file_unique_id}.jpg')


def gif_creator(message):
    """
    Creates gif animation with the help of Pilhandler
    :param message: tg response message
    :return:
    """
    picture_info = bot.get_file(message.photo[-1].file_id)
    path = f'{temp_path}/{picture_info.file_unique_id}.jpg'
    picture_file = bot.download_file(picture_info.file_path)
    with open(path, 'wb') as new_file:
        new_file.write(picture_file)
    GifPicture(message.media_group_id, message.from_user.id)


def gif_sender(message):
    """
    Sends created gif and saves it to minio storage
    :param message: tg response message
    :return:
    """
    file = f'{message.from_user.id}_{message.media_group_id}'
    io_file = open(f'{temp_path}/{file}.gif', 'rb')
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


def temp_clean():
    """
    Cleans temp storage
    :return:
    """
    for file in os.listdir(temp_path):
        file_path = os.path.join(temp_path, file)
        os.remove(file_path)
