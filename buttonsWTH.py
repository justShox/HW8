from telebot import types


def number_bt():
    user_contact = types.ReplyKeyboardMarkup(resize_keyboard=True)
    contact = types.KeyboardButton('Поделится контактом📲', request_contact=True)
    user_contact.add(contact)
    return user_contact


def location_bt():
    user_location = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location = types.KeyboardButton('Поделиться локацией📍', request_location=True)
    user_location.add(location)
    return user_location
