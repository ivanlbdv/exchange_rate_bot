import xml.etree.ElementTree as ET

import requests


def get_exchange_rate(val, date) -> str:
    value = float(
        ET.fromstring(
            requests.get(
                f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
            ).text
        ).find(
            f"./Valute[CharCode='{val}']/Value"
        ).text.replace(',', '.')
    )
    nominal = int(float(
        ET.fromstring(
            requests.get(
                f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
            ).text
        ).find(
            f"./Valute[CharCode='{val}']/Nominal"
        ).text.replace(',', '.')
    ))
    name = str(
        ET.fromstring(
            requests.get(
                f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
            ).text
        ).find(
            f"./Valute[CharCode='{val}']/Name"
        ).text.replace(',', '.')
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
    value = float(
        ET.fromstring(
            requests.get(
                f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
            ).text
        ).find(
            f"./Valute[CharCode='{val}']/Value"
        ).text.replace(',', '.')
    )

    nominal = int(float(
        ET.fromstring(
            requests.get(
                f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
            ).text
        ).find(
            f"./Valute[CharCode='{val}']/Nominal"
        ).text.replace(',', '.')
    ))
    if nominal == 1:
        return value
    else:
        value_div_nominal = value / nominal
        return value_div_nominal
