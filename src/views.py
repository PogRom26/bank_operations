import datetime
import json
from src.utils import (greeting,
                       total_summ_from_file,
                       top_transactions,
                       get_currency_rate, load_currencies_from_json,
                       get_stock_prices, load_stocks_from_json)


def operations_for_date(date_for_info) -> json:
    """Реализуйте набор функций и главную функцию,
    принимающую на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS
     и возвращающую JSON-ответ со следующими данными"""

    greeting_message = greeting()
    total_summ = total_summ_from_file(date_for_info)
    top_oper = top_transactions(date_for_info)
    currency = get_currency_rate(load_currencies_from_json())
    stock = get_stock_prices(load_stocks_from_json())
    total_info = greeting_message | total_summ | top_oper | currency | stock

    # Преобразование в JSON-строку
    json_data = json.dumps(total_info, ensure_ascii=False, indent=4)


    return json_data

print(operations_for_date("04.09.2021"))




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