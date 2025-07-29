import os
from datetime import datetime
from pathlib import Path

import openpyxl
import pandas as pd



def greeting():
    """Определяет какое сейчас время и выводит соответствующие приветствие"""

    current_time = datetime.now()

    if 6 < current_time.hour < 12:
        return "Доброе утро!"

    elif 12 < current_time.hour < 18:
        return "Добрые день!"

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


def last_four_digit_card(list_with_card):
  """По каждой карте: последние 4 цифры карты"""
  list_card_wo_stars = []

  for card in list_with_card:
    list_card_wo_stars.append(card[-4:])

  return list_card_wo_stars

x = card_list_with_stars()
print(last_four_digit_card(x))


def total_summ_spent():
  """По каждой карте: общая сумма расходов"""

  project_dir = Path(__file__).parent.parent
  data_dir = "data"
  file = 'operations.xlsx'
  file_path = os.path.join(project_dir, data_dir, file)

  df = pd.read_excel(file_path)
  total_spent = (df.groupby('Номер карты')['Сумма операции']
            .agg(lambda x: x.abs().sum())
            .reset_index()
            .sort_values('Сумма операции', ascending=False))

  return total_spent

print(total_summ_spent())


def total_summ_cashback():
  """По каждой карте: кешбэк (1 рубль на каждые 100 рублей)."""

  project_dir = Path(__file__).parent.parent
  data_dir = "data"
  file = 'operations.xlsx'
  file_path = os.path.join(project_dir, data_dir, file)

  df = pd.read_excel(file_path)

  total_cashback = (df.groupby('Номер карты')['Кэшбэк']
                 .agg(lambda x: x.abs().sum())
                 .reset_index()
                 .sort_values('Кэшбэк', ascending=False))


  return total_cashback

print(total_summ_cashback())








"""Топ-5 транзакций по сумме платежа.
Курс валют.
Стоимость акций из S&P500."""



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