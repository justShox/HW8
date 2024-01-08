import telebot
import buttons as bt
import database as db
from telebot.types import ReplyKeyboardRemove
from geopy import Nominatim

bot = telebot.TeleBot('6480576822:AAF4ypfj97ECwf2dzwu5P6sXNQNTVW1a9Vo')
# Для использования карт
geolocator = Nominatim(
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')


@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    check = db.checker(user_id)
    if message.text == '/start'.strip():
        if check:
            bot.send_message(user_id, f'С возвращением {message.from_user.first_name}!', reply_markup=bt.main_bt())
            bot.register_next_step_handler(message, calculator)
        else:
            bot.send_message(user_id, f'Здравствуйте {message.from_user.first_name}!'
                                      f'\nДавайте начнем регистрацию. Для начала напишите свое имя:')
            bot.register_next_step_handler(message, get_name)
    elif message.text == '/help':
        user_id = message.from_user.id
        bot.send_message(user_id, 'Вот вся информация по боту:'
                                  '\nЭтот бот предназначен для конвертации валюты(USD, EUR, UZS)'
                                  '\nПо курсу:'
                                  '\n1 доллар - 12,365 сум\n1 евро - 13,572 сум'
                                  '\nИсточник: https://www.google.com/finance/markets/currencies',
                         reply_markup=bt.main_bt())
        bot.register_next_step_handler(message, calculator)


def get_name(message):
    user_id = message.from_user.id
    name = message.text.strip().title()
    bot.send_message(user_id, f'Принято! Теперь поделитесь своим контактом:', reply_markup=bt.num_bt())
    bot.register_next_step_handler(message, contact, name)


def contact(message, name):
    user_id = message.from_user.id
    if message.contact:
        number = message.contact.phone_number
        bot.send_message(user_id, 'Отлично✅! И последнее поделитесь локацией', reply_markup=bt.loc_bt())
        bot.register_next_step_handler(message, location, name, number)
    else:
        bot.send_message(user_id, 'Пожалуйста поделитесь контактом😓', reply_markup=bt.num_bt())
        bot.register_next_step_handler(message, contact, name)


def location(message, name, number):
    user_id = message.from_user.id
    if message.location:
        loc = str(geolocator.reverse(f'{message.location.latitude}, '
                                     f'{message.location.longitude}'))
        db.registration(name, user_id, number, loc)
        bot.send_message(user_id, 'Готово! Вы зарегистрированы😊', reply_markup=bt.main_bt())
        bot.register_next_step_handler(message, calculator)

    else:
        bot.send_message(user_id, 'Пожалуйста поделитесь геопозицией🙃', reply_markup=bt.loc_bt())
        bot.register_next_step_handler(message, location, name, number)


@bot.message_handler(content_types=['text'])
def calculator(message):
    user_id = message.from_user.id
    if message.text == 'Калькулятор🧮'.strip():
        bot.send_message(user_id, 'Выберите валюту: ', reply_markup=bt.currency_bt())
    elif message.text == 'USD🇺🇸 - UZS🇺🇿'.strip():
        bot.send_message(user_id, 'Введите число: ')
        bot.register_next_step_handler(message, summa)
    elif message.text == 'USD🇺🇸 - EUR🇪🇺'.strip():
        bot.send_message(user_id, 'Введите число: ')
        bot.register_next_step_handler(message, summa1)
    elif message.text == 'UZS🇺🇿 - USD🇺🇸'.strip():
        bot.send_message(user_id, 'Введите число: ')
        bot.register_next_step_handler(message, summa2)
    elif message.text == 'UZS🇺🇿 - EUR🇪🇺'.strip():
        bot.send_message(user_id, 'Введите число: ')
        bot.register_next_step_handler(message, summa3)
    elif message.text == 'EUR🇪🇺 - USD🇺🇸'.strip():
        bot.send_message(user_id, 'Введите число: ')
        bot.register_next_step_handler(message, summa4)
    elif message.text == 'EUR🇪🇺 - UZS🇺🇿'.strip():
        bot.send_message(user_id, 'Введите число: ')
        bot.register_next_step_handler(message, summa5)
    elif message.text == '/help'.strip():
        user_id = message.from_user.id
        bot.send_message(user_id, 'Вот вся информация по боту:'
                                  '\nЭтот бот предназначен для конвертации валюты(USD, EUR, UZS)'
                                  '\nПо курсу:'
                                  '\n1 доллар - 12,365 сум\n1 евро - 13,572 сум'
                                  '\nИсточник: https://www.google.com/finance/markets/currencies',
                         reply_markup=bt.main_bt())
        bot.register_next_step_handler(message, calculator)
    elif message.text == '/start'.strip():
        user_id = message.from_user.id
        check = db.checker(user_id)
        if check:
            bot.send_message(user_id, f'С возвращением {message.from_user.first_name}!', reply_markup=bt.main_bt())
            bot.register_next_step_handler(message, calculator)
        else:
            bot.send_message(user_id, f'Здравствуйте {message.from_user.first_name}!'
                                      f'\nДавайте начнем регистрацию. Для начала напишите свое имя:')
            bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(user_id, 'Такая команда не поддерживается, введите /start')


def summa(message):
    global amount
    user_id = message.from_user.id
    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.send_message(user_id, 'Пожалуйста введите число!')
        bot.register_next_step_handler(message, summa)
        return
    count = amount * 12365
    bot.send_message(user_id, f'${amount} в суммах {round(count, 2)}, Можете ввести еще число',
                     reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, summa)


def summa1(message):
    global amount
    user_id = message.from_user.id
    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.send_message(user_id, 'Пожалуйста введите число!')
        bot.register_next_step_handler(message, summa1)
        return
    count = amount * 0.91
    bot.send_message(user_id, f'${amount} в евро = €{round(count, 2)}, Можете ввести еще число',
                     reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, summa1)


def summa2(message):
    global amount
    user_id = message.from_user.id
    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.send_message(user_id, 'Пожалуйста введите число!')
        bot.register_next_step_handler(message, summa2)
        return
    count = amount * 0.00008101
    bot.send_message(user_id, f'{amount} сумм в долларах = ${round(count, 2)}, Можете ввести еще число',
                     reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, summa2)


def summa3(message):
    global amount
    user_id = message.from_user.id
    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.send_message(user_id, 'Пожалуйста введите число!')
        bot.register_next_step_handler(message, summa3)
        return
    count = amount * 0.00007399
    bot.send_message(user_id, f'{amount} cумм в евро = €{round(count, 2)}, Можете ввести еще число',
                     reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, summa3)


def summa4(message):
    global amount
    user_id = message.from_user.id
    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.send_message(user_id, 'Пожалуйста введите число!')
        bot.register_next_step_handler(message, summa4)
        return
    count = amount * 1.09
    bot.send_message(user_id, f'€{amount} в долларах = ${round(count, 2)}, Можете ввести еще число',
                     reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, summa4)


def summa5(message):
    global amount
    user_id = message.from_user.id
    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.send_message(user_id, 'Пожалуйста введите число!')
        bot.register_next_step_handler(message, summa5)
        return
    count = amount * 13572
    bot.send_message(user_id, f'€{amount} в суммах = {round(count, 2)}, Можете ввести еще число',
                     reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, summa5)


bot.polling(none_stop=True)
