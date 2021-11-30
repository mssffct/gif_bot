import time

from telebot import types

from bot_handlers import (bot, get_gifs_command_handler, gif_creator,
                          gif_sender, text_to_picture_handler)
from keyboards import font_keyboard, main_keyboard


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
    get_gifs_command_handler(message)


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
    dict_fonts = {'Lobster': 'Lobster-Regular.ttf'}
    font = dict_fonts.get(message.text)
    if message.text == 'Lobster':
        font = 'Lobster-Regular.ttf'
    elif message.text == 'Comfortaa':
        font = 'Comfortaa-Medium.ttf'
    elif message.text == 'Comfortaa2':
        font = 'Comfortaa-Medium2.ttf'
    elif message.text == 'Comfortaa3':
        font = 'Comfortaa-Medium3.ttf'
    bot.send_message(
        message.from_user.id,
        'And now, add picture you want ',
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(message, create_picture, text, font)


def create_picture(message, text: str, font: str):
    try:
        if message.media_group_id is None and message.content_type == 'photo':
            text_to_picture_handler(message, text, font)
    except TypeError:
        bot.send_message(
            message.from_user.id,
            'Please add correct image'
        )
        bot.register_next_step_handler(message, create_picture, text, font)


@bot.message_handler(content_types=['photo'])
def create_gif(message):
    try:
        if message.media_group_id is not None:
            gif_creator(message)
        else:
            bot.send_message(
                message.from_user.id,
                'Please add two or more pictures'
            )
            bot.register_next_step_handler(message, create_gif)
    except TypeError:
        pass


def send_gif(message):
    time.sleep(10)
    try:
        gif_sender(message)
    except FileNotFoundError:
        bot.register_next_step_handler(message, send_gif)


if __name__ == '__main__':
    bot.infinity_polling(timeout=10)
