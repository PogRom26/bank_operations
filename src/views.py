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
    json_data = json.dumps(total_info, ensure_ascii=False, indent=2)


    return json_data

print(operations_for_date("04.09.2021"))
