from telebot import types

# MainKeyboard
picture_button = types.InlineKeyboardButton(
    text='Add text', callback_data='text'
)
gif_button = types.InlineKeyboardButton(
    text='Create gif', callback_data='gif'
)
main_keyboard = types.InlineKeyboardMarkup(row_width=2)\
    .add(picture_button, gif_button)

# FontKeyboard
lobster_button = types.KeyboardButton(
    text='Lobster'
)
comfortaa_button = types.KeyboardButton(
    text='Comfortaa'
)
font_keyboard = types.ReplyKeyboardMarkup(row_width=2)\
    .add(lobster_button, comfortaa_button)
