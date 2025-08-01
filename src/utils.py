import json
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv


def greeting(date: datetime = datetime.now()):
    """Определяет какое сейчас время и выводит соответствующие приветствие"""

    current_time = date.hour

    if 6 < current_time < 12:
        hello = {"greeting": "Доброе утро!"}
        return hello

    elif 12 < current_time < 18:
        hello = {"greeting": "Добрый день!"}
        return hello

    elif 18 < current_time < 24:
        hello = {"greeting": "Добрый вечер!"}
        return hello

    else:
        hello = {"greeting": "Доброй ночи!"}
        return hello


def get_dataframe():
    """Определяет файл и создает по нему DataFrame для дальнейшего использования другими функциями"""

    # Загрузка данных
    project_dir = Path(__file__).parent.parent
    data_dir = "data"
    file = "operations.xlsx"
    file_path = os.path.join(project_dir, data_dir, file)

    df = pd.read_excel(file_path)

    return df


def data_frame_filtered_by_date(user_date: str = "04.09.2021"):
    """Использует базовый DataFrame и применяет к нему фильтрацию по дате,
    возвращая DataFrame с операциями, отобранными по дате"""

    df = get_dataframe()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    df["Сумма кэшбэка"] = round((df["Сумма платежа"] / 100), 2)

    # Преобразуем в datetime объект
    if isinstance(user_date, str):
        date_obj = datetime.strptime(user_date, "%d.%m.%Y")
    else:
        date_obj = user_date

    # Начало и конец месяца
    start_of_month = date_obj.replace(day=1)
    end_of_month = date_obj + relativedelta(day=31)

    filtered_data = df[(df["Дата операции"] >= start_of_month) & (df["Дата операции"] <= end_of_month)]

    return filtered_data


def total_summ_from_file(user_date: str = "04.09.2021"):
    """Принимает DataFrame.
    Считает общую сумму платежей и кешбэк по каждой карте.
    Выводит информацию о номере карты (последние 4 цифры), сумму расходов по карте и сумму кэшбэка"""

    filtered_data = data_frame_filtered_by_date()

    # Считаем суммы расходов по картам
    total_spent = (
        filtered_data.groupby("Номер карты")["Сумма платежа"]
        .agg(lambda x: round(abs(x).sum(), 2))
        .reset_index()
        .sort_values("Сумма платежа", ascending=True)
    )

    # Считаем суммы кэшбэка по картам
    cash_back = (
        filtered_data.groupby("Номер карты")["Сумма кэшбэка"]
        .agg(lambda x: round(abs(x).sum(), 2))
        .reset_index()
        .sort_values("Сумма кэшбэка", ascending=True)
    )

    # Объединяем суммы расходов и суммы кэшбэка
    merged_df = pd.merge(total_spent, cash_back, on="Номер карты")

    merged_df_to_dict = merged_df.to_dict("records")

    cards = {"card": merged_df_to_dict}

    transformed_data = {
        "card": [
            {
                "last_digits": card["Номер карты"].replace("*", ""),
                "total_spent": card["Сумма платежа"],
                "cashback": card["Сумма кэшбэка"],
            }
            for card in cards["card"]
        ]
    }

    return transformed_data


def top_transactions(user_date: str = "04.09.2021"):
    """Принимает отфильтрованный DataFrame.
    Выводит информацию о Топ-5 транзакций по сумме платежа."""

    filtered_data = data_frame_filtered_by_date()

    top_5 = filtered_data.nlargest(5, "Сумма платежа")[["Дата платежа", "Сумма платежа", "Категория", "Описание"]]

    merged_df_to_dict = top_5.to_dict("records")

    list_top_transactions = {"top_transactions": merged_df_to_dict}

    # Словарь для маппинга русских ключей на английские
    key_mapping = {
        "Дата платежа": "date",
        "Сумма платежа": "amount",
        "Категория": "category",
        "Описание": "description",
    }

    # Преобразование данных
    transformed_data = {
        "top_transactions": [
            {key_mapping[rus_key]: value for rus_key, value in transaction.items()}
            for transaction in list_top_transactions["top_transactions"]
        ]
    }

    return transformed_data


def get_currency_rate(currencies: list) -> any:
    """Принимает список валют из файла user_settings.json.
    Обращается по каждой валюте через API для получения актуального курса по отношению к рублю.
    Возвращает список с указанием валюты и самого курса"""

    # Загрузка данных для обращения к API
    load_dotenv()
    api_key = os.getenv("API_KEY_FOR_CURRENCY")
    headers = {"apikey": api_key}

    # Определение валют. Рубль по умолчанию.
    to = "RUB"

    amount = 1

    result_list = {}

    for currency in currencies:
        from_str = currency

        # Адрес для обращения
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={to}&from={from_str}&amount={amount}"

        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            result_list[currency] = round((data["result"]), 2)
        else:
            print(response.status_code)

    total_list = {"currency_rates": result_list}

    transformed_data = {
        "currency_rates": [
            {"currency": currency, "rate": rate} for currency, rate in total_list["currency_rates"].items()
        ]
    }

    return transformed_data


def load_currencies_from_json() -> list:
    """Функция загружает список валют из JSON файла для дальнейшей обработки"""

    # Загрузка данных
    project_dir = Path(__file__).parent.parent
    file = "user_settings.json"
    file_path = os.path.join(project_dir, file)

    with open(file_path, "r") as f:
        data = json.load(f)
        return data.get("user_currencies", [])


def get_stock_prices(stocks: list) -> any:
    """Принимает список акций из файла user_settings.json.
      Обращается по каждой валюте через API для получения актуального курса по отношению к рублю.
      Возвращает список с указанием валюты и самого курса

    Стоимость акций из S&P500."""

    # Загрузка данных для обращения к API
    load_dotenv()
    api_key = os.getenv("API_KEY_FOR_STOCK")
    url = f"https://api.marketstack.com/v1/eod/latest?access_key={api_key}"

    result_list = {}

    for stock in stocks:
        querystring = {"symbols": stock}
        response = requests.get(url, params=querystring)

        if response.status_code == 200:
            data = response.json()
            result_list[stock] = data["data"][0]["close"]
        else:
            print(response.status_code)

    total_list = {"stock_prices": result_list}

    transformed_data = {
        "stock_prices": [{"stock": currency, "price": rate} for currency, rate in total_list["stock_prices"].items()]
    }

    return transformed_data


def load_stocks_from_json() -> list:
    """Функция загружает список акций из JSON файла для дальнейшей обработки"""
    # Загрузка данных
    project_dir = Path(__file__).parent.parent
    file = "user_settings.json"
    file_path = os.path.join(project_dir, file)

    with open(file_path, "r") as f:
        data = json.load(f)
        return data.get("user_stocks", [])
