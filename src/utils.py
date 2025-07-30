import json
import os
from datetime import datetime
from pathlib import Path
from dateutil.relativedelta import relativedelta
import requests
from dotenv import load_dotenv

import openpyxl
import pandas as pd



def greeting(date:datetime = datetime.now()):
    """Определяет какое сейчас время и выводит соответствующие приветствие"""

    current_time = datetime.now()

    if 6 < current_time.hour < 12:
        return "Доброе утро!"

    elif 12 < current_time.hour < 18:
        return "Добрый день!"

    elif 18 < current_time.hour < 24:
        return "Добрый вечер!"

    else:
        return "Доброй ночи!"


def card_list_with_stars():
  """Возвращает список карт со звездами (как есть в документе)"""

  project_dir = Path(__file__).parent.parent
  data_dir = "data"
  file = 'operations.xlsx'
  file_path = os.path.join(project_dir, data_dir, file)

  df = pd.read_excel(file_path)

  # Извлекаем уникальные номера карт
  card_numbers_list = df['Номер карты'].unique().tolist()
  card_list_w_stars = []

  for card in card_numbers_list:
    if type(card) == str:
      card_list_w_stars.append(card)

  return card_list_w_stars

# print(card_list_with_stars())


def last_four_digit_card(list_with_card):
  """По каждой карте: последние 4 цифры карты"""
  list_card_wo_stars = []

  for card in list_with_card:
    list_card_wo_stars.append(card[-4:])

  return list_card_wo_stars

# x = card_list_with_stars()
# print(last_four_digit_card(x))


def total_summ_from_file(user_date:str = "04.09.2021"):

  # Загрузка данных
  project_dir = Path(__file__).parent.parent
  data_dir = "data"
  file = 'operations.xlsx'
  file_path = os.path.join(project_dir, data_dir, file)

  df = pd.read_excel(file_path)
  df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)
  df['Сумма кэшбэка'] = round((df['Сумма платежа'] / 100), 2)

  # Преобразуем в datetime объект
  if isinstance(user_date, str):
    date_obj = datetime.strptime(user_date, "%d.%m.%Y")
  else:
    date_obj = user_date

  # Начало и конец месяца
  start_of_month = date_obj.replace(day=1)
  end_of_month = date_obj + relativedelta(day=31)

  # print(f"Начало месяца: {start_of_month.strftime('%d.%m.%Y')}")
  # print(f"Конец месяца: {end_of_month.strftime('%d.%m.%Y')}")

  filtered_data = df[(df['Дата операции'] >= start_of_month) & (df['Дата операции'] <= end_of_month)]

  # Считаем суммы расходов по картам
  total_spent = (filtered_data.groupby('Номер карты')['Сумма платежа']
            .agg(lambda x: x.sum())
            .reset_index()
            .sort_values('Сумма платежа', ascending=True))

  # Считаем суммы кэшбэка по картам
  cash_back = (filtered_data.groupby('Номер карты')['Сумма кэшбэка']
            .agg(lambda x: x.sum())
            .reset_index()
            .sort_values('Сумма кэшбэка', ascending=True))

  # Объединяем суммы расходов и суммы кэшбэка
  merged_df = pd.merge(total_spent, cash_back, on='Номер карты')

  return merged_df

# print(total_summ_from_file("01.06.2020"))


def top_transactions (user_date:str = "04.09.2021"):
  """Топ-5 транзакций по сумме платежа."""
  # Загрузка данных
  project_dir = Path(__file__).parent.parent
  data_dir = "data"
  file = 'operations.xlsx'
  file_path = os.path.join(project_dir, data_dir, file)

  df = pd.read_excel(file_path)
  df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)

  # Преобразуем в datetime объект
  if isinstance(user_date, str):
    date_obj = datetime.strptime(user_date, "%d.%m.%Y")
  else:
    date_obj = user_date

  # Начало и конец месяца
  start_of_month = date_obj.replace(day=1)
  end_of_month = date_obj + relativedelta(day=31)

  filtered_data = df[(df['Дата операции'] >= start_of_month) & (df['Дата операции'] <= end_of_month)]

  top_5 = filtered_data.nlargest(5, 'Сумма платежа')[['Дата платежа', 'Сумма платежа', 'Категория', 'Описание']]

  return top_5

# print(top_transactions("11.12.2021"))


def get_currency_rate(currencies: list) -> any:
  """Курс валют"""

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

  return result_list

# list_w_currency = {"USD", "EUR"}
# print(get_currency_rate(list(list_w_currency)))


def load_currencies_from_json() -> list:
  """Загружает список валют из JSON файла"""
  # Загрузка данных
  project_dir = Path(__file__).parent.parent
  file = 'user_settings.json'
  file_path = os.path.join(project_dir, file)

  with open(file_path, 'r') as f:
    data = json.load(f)
    return data.get('user_currencies', [])

# print(load_currencies_from_json())

# print("Курсы валют к RUB:")
# print(get_currency_rate(load_currencies_from_json()))


def get_stock_prices(stocks: list) -> any:
  """Стоимость акций из S&P500."""

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

  return result_list


def load_stocks_from_json() -> list:
  """Загружает список акций из JSON файла"""
  # Загрузка данных
  project_dir = Path(__file__).parent.parent
  file = 'user_settings.json'
  file_path = os.path.join(project_dir, file)

  with open(file_path, 'r') as f:
    data = json.load(f)
    return data.get('user_stocks', [])


# print(get_stock_prices(load_stocks_from_json()))








var = {
  "greeting": "Добрый день",
  "cards": [
    {
      "last_digits": "5814",
      "total_spent": 1262.00,
      "cashback": 12.62
    },
    {
      "last_digits": "7512",
      "total_spent": 7.94,
      "cashback": 0.08
    }
  ],
  "top_transactions": [
    {
      "date": "21.12.2021",
      "amount": 1198.23,
      "category": "Переводы",
      "description": "Перевод Кредитная карта. ТП 10.2 RUR"
    },
    {
      "date": "20.12.2021",
      "amount": 829.00,
      "category": "Супермаркеты",
      "description": "Лента"
    },
    {
      "date": "20.12.2021",
      "amount": 421.00,
      "category": "Различные товары",
      "description": "Ozon.ru"
    },
    {
      "date": "16.12.2021",
      "amount": -14216.42,
      "category": "ЖКХ",
      "description": "ЖКУ Квартира"
    },
    {
      "date": "16.12.2021",
      "amount": 453.00,
      "category": "Бонусы",
      "description": "Кешбэк за обычные покупки"
    }
  ],
  "currency_rates": [
    {
      "currency": "USD",
      "rate": 73.21
    },
    {
      "currency": "EUR",
      "rate": 87.08
    }
  ],
  "stock_prices": [
    {
      "stock": "AAPL",
      "price": 150.12
    },
    {
      "stock": "AMZN",
      "price": 3173.18
    },
    {
      "stock": "GOOGL",
      "price": 2742.39
    },
    {
      "stock": "MSFT",
      "price": 296.71
    },
    {
      "stock": "TSLA",
      "price": 1007.08
    }
  ]
}