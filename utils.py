import xml.etree.ElementTree as ET

import requests


def get_exchange_rate(val, date):
    try:
        request = requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}')
        if request.status_code != 200:
            raise Exception(f'Ошибка при запросе к API: {request.status_code}')
        value = float(
            ET.fromstring(request.text)
            .find(f"./Valute[CharCode='{val}']/Value")
            .text
            .replace(',', '.')
        )
        nominal = int(float(
            ET.fromstring(request.text)
            .find(f"./Valute[CharCode='{val}']/Nominal")
            .text
            .replace(',', '.')
        ))
        name = str(
            ET.fromstring(request.text)
            .find(f"./Valute[CharCode='{val}']/Name")
            .text
            .replace(',', '.')
        )

        if nominal == 1:
            return (
                f'Курс {val} на {date} (ЦБ РФ):'
                "\n"
                f'{nominal} {name} = {value} RUB.'
                "\n\nДля повторения запроса выберите действие из меню."
                )
        else:
            value_div_nominal = round(value / nominal, 4)
            return (
                f'Курс {val} на {date} (ЦБ РФ):'
                "\n"
                f'{nominal} {name} = {value} RUB'
                "\n"
                f'(1 {val} ≈ {value_div_nominal} RUB).'
                "\n\nДля повторения запроса выберите действие из меню."
                )
    except requests.exceptions.RequestException:
        return ('Произошла ошибка при запросе к API. '
                'Пожалуйста, попробуйте позже.\n\n'
                'Для повторения запроса выберите действие из меню.')
    except Exception:
        return ('Произошла непредвиденная ошибка.\n\n'
                'Для повторения запроса выберите действие из меню.')


def get_exchange_rate_converter(val, date):
    request = requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}')
    value = float(
        ET.fromstring(request.text)
        .find(f"./Valute[CharCode='{val}']/Value")
        .text
        .replace(',', '.')
    )
    nominal = int(float(
        ET.fromstring(request.text)
        .find(f"./Valute[CharCode='{val}']/Nominal")
        .text
        .replace(',', '.')
    ))
    if nominal == 1:
        return value
    else:
        value_div_nominal = value / nominal
        return value_div_nominal
