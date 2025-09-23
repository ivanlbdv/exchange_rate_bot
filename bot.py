import os
import re
from datetime import date, timedelta

import telebot
from dotenv import load_dotenv
from telebot import types


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
        "или введите свой в формате ДД.ММ.ГГГГ."
        ), reply_markup=markup)
    bot.register_next_step_handler(msg,
                                   get_date_curr_exchange_rate,
                                   valute_date)


def get_date_curr_exchange_rate(message, valute_date):
    valute_date['date_rate'] = message.text
    try:
        bot.send_message(message.chat.id,
                         f'{get_exchange_rate(valute_date["valute"], valute_date["date_rate"])}'
                         )
    except:
        # TODO Сделать проверку на корректно введенную дату,
        # учитывая количество дней в месяце.
        pattern = r'\d{2}\.\d{2}\.\d{4}'
        if not re.fullmatch(pattern, message.text):
            bot.send_message(message.chat.id, (
                "Вы указали несуществующую дату.\n\n"
                "Для повторения запроса выберите действие из меню."
                ))
        else:
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
        "или введите свой в формате ДД.ММ.ГГГГ."
        ), reply_markup=markup)
    bot.register_next_step_handler(
        msg, get_date_converter,
        valute_date_value_dir
    )


def get_date_converter(message, valute_date_value_dir):
    valute_date_value_dir['date_rate'] = message.text
    msg = bot.send_message(message.chat.id, 'Укажите сумму для конвертации.')
    bot.register_next_step_handler(
        msg,
        get_value_converter,
        valute_date_value_dir
    )


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


def get_exchange_rate(val, date) -> str:
    import xml.etree.ElementTree as ET

    import requests
    value = float(
        ET.fromstring(requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}').text)
        .find(f"./Valute[CharCode='{val}']/Value")
        .text.replace(',', '.')
    )
    nominal = int(float(
        ET.fromstring(requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}').text)
        .find(f"./Valute[CharCode='{val}']/Nominal")
        .text.replace(',', '.')
    ))
    name = str(
        ET.fromstring(requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}').text)
        .find(f"./Valute[CharCode='{val}']/Name")
        .text.replace(',', '.')
    )

    if nominal == 1:
        return (
            f'Курс {val} на {date} (ЦБ РФ):'
            "\n"
            f'{nominal} {name} = {value} RUB.'
            "\n\nДля повторения запроса выберите действие из меню."
            )
    else:
        value_div_nominal = round(value / nominal, 2)
        return (
            f'Курс {val} на {date} (ЦБ РФ):'
            "\n"
            f'{nominal} {name} = {value} RUB'
            "\n"
            f'(1 {val} ≈ {value_div_nominal} RUB).'
            "\n\nДля повторения запроса выберите действие из меню."
            )


def get_exchange_rate_converter(val, date) -> float:
    import xml.etree.ElementTree as ET

    import requests
    value = float(
        ET.fromstring(requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}').text)
        .find(f"./Valute[CharCode='{val}']/Value")
        .text.replace(',', '.')
    )
    nominal = int(float(
        ET.fromstring(requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}').text)
        .find(f"./Valute[CharCode='{val}']/Nominal")
        .text.replace(',', '.')
    ))
    name = str(
        ET.fromstring(requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}').text)
        .find(f"./Valute[CharCode='{val}']/Name")
        .text.replace(',', '.')
    )
    if nominal == 1:
        return value
    else:
        value_div_nominal = value / nominal
        return value_div_nominal



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
