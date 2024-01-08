import telebot
import buttonsWTH as bt
import databaseWTH as db
from geopy import Nominatim
from telebot.types import ReplyKeyboardRemove
import json
import requests

bot = telebot.TeleBot('6833110655:AAHwDhNRr5PO7KvMA-THdqIs5LdzGhBVReI')

# Для локации
geolocator = Nominatim(
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

# Для погоды
API = '04ce9501ff1973178da581c5d24d4b4f'


@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    check = db.checker(user_id)
    if check:
        bot.send_message(user_id, f'С возвращением {message.from_user.first_name}☺️!'
                                  f'\nВведите любой город, чтоб узнать погоду🙃:')
        bot.register_next_step_handler(message, get_weather)
    else:
        bot.send_message(user_id, f'Здравствуйте {message.from_user.first_name}👋🏻'
                                  f'\nДавайте начнем регистрацию. Напишите мне свое имя😀:')
        bot.register_next_step_handler(message, get_name)

@bot.message_handler(commands=['help'])

def get_name(message):
    user_id = message.from_user.id
    name = message.text.title().strip()
    bot.send_message(user_id, 'Хорошо! Теперь поделитесь контактом😃:',
                     reply_markup=bt.number_bt())
    bot.register_next_step_handler(message, get_contact, name)


def get_contact(message, name):
    user_id = message.from_user.id
    if message.contact:
        number = message.contact.phone_number
        bot.send_message(user_id, 'Ага! И последнее осталось ваша локация😉:',
                         reply_markup=bt.location_bt())
        bot.register_next_step_handler(message, get_location, name, number)
    else:
        bot.send_message(user_id, 'Пожалуйста поделитесь контактом😕', reply_markup=bt.number_bt())
        bot.register_next_step_handler(message, get_contact, name)


def get_location(message, name, number):
    user_id = message.from_user.id
    if message.location:
        location = str(geolocator.reverse(f'{message.location.latitude},{message.location.longitude}'))
        db.registration(user_id, name, number, location)
        bot.send_message(user_id, 'Получилось! Вы зарегистрированы😊.'
                                  '\nВведите любой город, чтоб узнать погоду🙃:', reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_weather)
    else:
        bot.send_message(user_id, 'Пожалуйста поделитесь локацией🫤', reply_markup=bt.location_bt())
        bot.register_next_step_handler(message, name, number, get_location)


def get_weather(message):
    user_id = message.from_user.id
    if message.text:
        city = message.text.strip().title()
        info = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
        if info.status_code == 200:
            weather = json.loads(info.text)
            bot.send_message(user_id, f'Информация о {weather["name"]}, {weather["sys"]["country"]}'
                                      f'\n'
                                      f'\n Температура🌡: {weather["main"]["temp"]}°С,'
                                      f'\n Ощущается как😮‍💨: {weather["main"]["feels_like"]}°С'
                                      f'\n Влажность💦: {weather["main"]["humidity"]}%'
                                      f'\n Давление🫨: {weather["main"]["pressure"]}гПа'
                                      f'\n Скорость ветра🌬: {weather["wind"]["speed"]}м/с'
                                      f'\n Видимость👁: {weather["visibility"]} м'
                                      f'\n\nВведите еще город:')
            bot.register_next_step_handler(message, get_weather)
        else:
            bot.send_message(user_id, 'Города не найден😓!')
            bot.register_next_step_handler(message, get_weather)
    else:
        bot.send_message(user_id, 'Я вас не понимаю🤨!')
        bot.register_next_step_handler(message, get_weather)


bot.polling(none_stop=True)
