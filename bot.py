import os
import re
import xml.etree.ElementTree as ET
from datetime import date, timedelta

import telebot
from dotenv import load_dotenv
from telebot import types

from utils import get_exchange_rate, get_exchange_rate_converter

load_dotenv()

token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, (
            "Выберите действие:\n\n"
            "Курсы валют: /curr_exchange_rate\n"
            "Конвертер валют: /converter"
            ))


@bot.message_handler(commands=['curr_exchange_rate'])
def main_curr_exchange_rate(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                       one_time_keyboard=True)
    button_usd = types.KeyboardButton('USD')
    button_eur = types.KeyboardButton('EUR')
    button_cny = types.KeyboardButton('CNY')
    button_kzt = types.KeyboardButton('KZT')
    button_try = types.KeyboardButton('TRY')
    button_aed = types.KeyboardButton('AED')
    button_byn = types.KeyboardButton('BYN')
    button_jpy = types.KeyboardButton('JPY')
    button_uzs = types.KeyboardButton('UZS')
    markup.add(button_usd, button_eur, button_cny)
    markup.add(button_kzt, button_try, button_aed)
    markup.add(button_byn, button_jpy, button_uzs)
    msg = bot.send_message(message.chat.id, (
        "Укажите код валюты.\n\n"
        "Выберите доступные варианты кодов валют ниже или введите свой.\n\n"
        "Буквенные коды валют, курс которых устанавливается ЦБ РФ, "
        "указаны на сайте https://cbr.ru/currency_base/daily/."
        ), reply_markup=markup)
    bot.register_next_step_handler(msg, get_valute_curr_exchange_rate)


def get_valute_curr_exchange_rate(message):
    valute_date = {}
    valute_date['valute'] = message.text.upper()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                       one_time_keyboard=True)
    button_yesterday = types.KeyboardButton(
        (f'{(date.today() - timedelta(days=1)).strftime("%d.%m.%Y")}')
        )
    button_today = types.KeyboardButton(
        (f'{(date.today()).strftime("%d.%m.%Y")}')
        )
    button_tomorrow = types.KeyboardButton(
        (f'{(date.today() + timedelta(days=1)).strftime("%d.%m.%Y")}')
        )
    markup.add(button_yesterday, button_today, button_tomorrow)
    msg = bot.send_message(message.chat.id, (
        "Укажите дату, на которую необходимо получить курс "
        f'{valute_date["valute"]}.'
        "\n\n"
        "Выберите доступные варианты дат ниже "
        "или введите свой в формате 'ДД.ММ.ГГГГ'."
        ), reply_markup=markup)
    bot.register_next_step_handler(msg,
                                   get_date_curr_exchange_rate,
                                   valute_date)


def get_date_curr_exchange_rate(message, valute_date):
    valute_date['date_rate'] = message.text
    pattern = re.compile(
        r'^('
        r'(0[1-9]|1[0-9]|2[0-8])\.(0[1-9]|1[0-2])\.\d{4}|'
        r'(29|30)\.(0[13578]|1[02])\.\d{4}|'
        r'31\.(0[13578]|1[02])\.\d{4}|'
        r'29\.02\.(?:'
        r'(?:[02468][048]|[13579][26])00|'
        r'(?:\d\d)(?:[02468][048]|[13579][26])'
        r'))$'
    )
    try:
        if not re.fullmatch(pattern, message.text):
            raise ValueError('Некорректный формат даты.')

        bot.send_message(message.chat.id,
                         f'{get_exchange_rate(valute_date["valute"], valute_date["date_rate"])}'
                         )
    except ValueError:
        bot.send_message(message.chat.id, (
            "Вы указали несуществующую дату.\n\n"
            "Для повторения запроса выберите действие из меню."
            ))
    except Exception:
        bot.send_message(message.chat.id, (
            "Вы указали несуществующий код валюты или курс "
            f'{valute_date["valute"]} на {valute_date["date_rate"]}'
            " ЦБ РФ еще не установлен.\n\n"
            "Для повторения запроса выберите действие из меню."
            ))


@bot.message_handler(commands=['converter'])
def main_converter(message):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
    button_usd = types.KeyboardButton('USD')
    button_eur = types.KeyboardButton('EUR')
    button_cny = types.KeyboardButton('CNY')
    button_kzt = types.KeyboardButton('KZT')
    button_try = types.KeyboardButton('TRY')
    button_aed = types.KeyboardButton('AED')
    button_byn = types.KeyboardButton('BYN')
    button_jpy = types.KeyboardButton('JPY')
    button_uzs = types.KeyboardButton('UZS')
    markup.add(button_usd, button_eur, button_cny)
    markup.add(button_kzt, button_try, button_aed)
    markup.add(button_byn, button_jpy, button_uzs)
    msg = bot.send_message(message.chat.id, (
        "Укажите код валюты.\n\n"
        "Выберите доступные варианты кодов валют ниже или введите свой.\n\n"
        "Буквенные коды валют, курс которых устанавливается ЦБ РФ, "
        "указаны на сайте https://cbr.ru/currency_base/daily/."
        ), reply_markup=markup)
    bot.register_next_step_handler(msg, get_valute_converter)


def get_valute_converter(message):
    valute_date_value_dir = {}
    valute_date_value_dir['valute'] = message.text.upper()
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
    button_yesterday = types.KeyboardButton(
        f'{(date.today() - timedelta(days=1)).strftime("%d.%m.%Y")}'
    )
    button_today = types.KeyboardButton(
        f'{(date.today()).strftime("%d.%m.%Y")}'
    )
    button_tomorrow = types.KeyboardButton(
        f'{(date.today() + timedelta(days=1)).strftime("%d.%m.%Y")}'
    )
    markup.add(button_yesterday, button_today, button_tomorrow)
    msg = bot.send_message(message.chat.id, (
        f'Укажите дату курса {valute_date_value_dir["valute"]}'
        " для конвертации валюты.\n\n"
        "Выберите доступные варианты дат ниже "
        "или введите свой в формате 'ДД.ММ.ГГГГ'."
        ), reply_markup=markup)
    bot.register_next_step_handler(
        msg, get_date_converter,
        valute_date_value_dir
    )


def get_date_converter(message, valute_date_value_dir):
    valute_date_value_dir['date_rate'] = message.text
    pattern = re.compile(
        r'^('
        r'(0[1-9]|1[0-9]|2[0-8])\.(0[1-9]|1[0-2])\.\d{4}|'
        r'(29|30)\.(0[13578]|1[02])\.\d{4}|'
        r'31\.(0[13578]|1[02])\.\d{4}|'
        r'29\.02\.(?:'
        r'(?:[02468][048]|[13579][26])00|'
        r'(?:\d\d)(?:[02468][048]|[13579][26])'
        r'))$'
    )
    try:
        if not re.fullmatch(pattern, message.text):
            raise ValueError('Некорректный формат даты.')
        msg = bot.send_message(message.chat.id, 'Укажите сумму для конвертации.')
        bot.register_next_step_handler(
            msg,
            get_value_converter,
            valute_date_value_dir
        )
    except ValueError:
        bot.send_message(message.chat.id, (
            "Вы указали несуществующую дату.\n\n"
            "Для повторения запроса выберите действие из меню."
            ))


def get_value_converter(message, valute_date_value_dir):
    pattern = r'(\d+)|(\d+(\.|\,)\d+)'
    if not re.fullmatch(pattern, message.text):
        bot.send_message(message.chat.id, (
            "Для конвертации необходимо ввести число.\n\n"
            "Для повторения запроса выберите действие из меню."
            ))
    else:
        valute_date_value_dir['value'] = message.text.replace(',', '.')
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
        )
        button_rub_to_curr = f'RUB  >>  {valute_date_value_dir["valute"]}'
        button_curr_to_rub = f'{valute_date_value_dir["valute"]}  >>  RUB'
        markup.add(button_rub_to_curr, button_curr_to_rub)
        msg = bot.send_message(
            message.chat.id,
            'Укажите направление конвертации.',
            reply_markup=markup
        )
        bot.register_next_step_handler(
            msg,
            get_direction_converter,
            valute_date_value_dir
        )


def get_direction_converter(message, valute_date_value_dir):
    valute_date_value_dir['dir'] = message.text
    try:
        if valute_date_value_dir['dir'] == f'RUB  >>  {valute_date_value_dir["valute"]}':
            bot.send_message(message.chat.id, (
                f'{valute_date_value_dir["value"]} RUB = {round(float(valute_date_value_dir["value"]) / get_exchange_rate_converter(valute_date_value_dir["valute"], valute_date_value_dir["date_rate"]), 4)} {valute_date_value_dir["valute"]}.'
                "\n\n"
                "Для повторения запроса выберите действие из меню."
                ))
        if valute_date_value_dir['dir'] == f'{valute_date_value_dir["valute"]}  >>  RUB':
            bot.send_message(message.chat.id, (
                f'{valute_date_value_dir["value"]} {valute_date_value_dir["valute"]} = {round(float(valute_date_value_dir["value"]) * get_exchange_rate_converter(valute_date_value_dir["valute"], valute_date_value_dir["date_rate"]), 4)} RUB.'
                "\n\n"
                "Для повторения запроса выберите действие из меню."
                ))
    except AttributeError:
        bot.send_message(message.chat.id, (
            "Вы указали несуществующий код валюты или курс "
            f'{valute_date_value_dir["valute"]} на {valute_date_value_dir["date_rate"]}'
            " ЦБ РФ еще не установлен.\n\n"
            "Для повторения запроса выберите действие из меню."
            ))
    except ET.ParseError:
        bot.send_message(message.chat.id, (
            'Произошла ошибка при запросе к API. '
            'Пожалуйста, попробуйте позже.\n\n'
            'Для повторения запроса выберите действие из меню.'
        ))


@bot.message_handler(content_types=['text'])
def say_hi(message):
    bot.send_message(message.chat.id, (
        "Выберите действие из меню."
        )
    )


def main():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
