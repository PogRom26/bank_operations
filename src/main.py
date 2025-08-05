# import json
# import os
# from datetime import datetime
# from pathlib import Path
#
# import pandas as pd
# import requests
# from dateutil.relativedelta import relativedelta
# from dotenv import load_dotenv
# from pandas.io.formats.format import return_docstring
#
# from src.utils import (get_currency_rate, get_stock_prices, greeting, load_currencies_from_json, load_stocks_from_json,
#                        top_transactions, total_summ_from_file)
#
#
# def all_func(date_for_info):
#     """Функция собирает вместе всю информацию по другим функциям"""
#
#     greeting_message = greeting()
#     total_summ = total_summ_from_file(date_for_info)
#     top_oper = top_transactions(date_for_info)
#     currency = get_currency_rate(load_currencies_from_json())
#     stock = get_stock_prices(load_stocks_from_json())
#     total_info = greeting_message | total_summ | top_oper | currency | stock
#
#     # Преобразование в JSON-строку
#     json_data = json.dumps(total_info, ensure_ascii=False, indent=2)
#
#     return json_data
#
# print(all_func("01.09.2021"))

