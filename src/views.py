"""Функция для страницы «Главная» отдает корректный JSON-ответ согласно ТЗ"""
import datetime
import json
from src.utils import greeting

def operations_for_date() -> json:
    """Реализуйте набор функций и главную функцию,
    принимающую на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS
     и возвращающую JSON-ответ со следующими данными"""
    return greeting()


print(operations_for_date())

print(datetime.datetime.now())