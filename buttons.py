from telebot import types


def num_bt():
    user_contact = types.ReplyKeyboardMarkup(resize_keyboard=True)
    contact = types.KeyboardButton('Поделиться контактом📱', request_contact=True)
    user_contact.add(contact)
    return user_contact


def loc_bt():
    user_location = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location = types.KeyboardButton('Поделиться геопозицией📍', request_location=True)
    user_location.add(location)
    return user_location


def main_bt():
    main_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    calculator = types.KeyboardButton('Калькулятор🧮')
    # currency_converter = types.KeyboardButton('Конвертер валют💵') # В разработке
    main_buttons.add(calculator)
    return main_buttons


def currency_bt():
    currency_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    usd1 = types.KeyboardButton('USD🇺🇸 - UZS🇺🇿')
    usd2 = types.KeyboardButton('USD🇺🇸 - EUR🇪🇺')
    eur1 = types.KeyboardButton('EUR🇪🇺 - USD🇺🇸')
    eur2 = types.KeyboardButton('EUR🇪🇺 - UZS🇺🇿')
    uzs1 = types.KeyboardButton('UZS🇺🇿 - USD🇺🇸')
    uzs2 = types.KeyboardButton('UZS🇺🇿 - EUR🇪🇺')
    currency_button.add(usd1, usd2, eur1, eur2, uzs1, uzs2)
    return currency_button
