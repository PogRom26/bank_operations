"""Функция для страницы «Главная» отдает корректный JSON-ответ согласно ТЗ"""
import datetime
import json
from src.utils import greeting

def operations_for_date(date) -> json:
    """Реализуйте набор функций и главную функцию,
    принимающую на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS
     и возвращающую JSON-ответ со следующими данными"""
    x = greeting(date)
    return x


print(operations_for_date("2025-07-29 19:26:15.665265"))

# print(datetime.datetime.now())