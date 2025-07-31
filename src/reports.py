from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional
import pandas as pd
from src.utils import get_dataframe
from functools import wraps
from pathlib import Path
import os


def save_results_to_file(filename):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Выполняем оригинальную функцию и получаем результат
            result = func(*args, **kwargs)

            # Строим путь к файлу относительно корневого каталога проекта
            project_dir = Path(__file__).parent.parent
            data_dir = "data"
            full_filename = os.path.join(project_dir, data_dir, filename)

            # Создаем каталог, если он не существует
            directory = os.path.dirname(full_filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # Записываем результат в файл
            with open(full_filename, mode='w', encoding='utf-8') as file:
                output_line = f"{func.__name__} ({args}) => {result}\n"
                file.write(output_line)

            return result
        return wrapper
    return decorator


@save_results_to_file("spending_by_category.json")
def spending_by_category(category: str,

                         date: Optional[str] = None) -> pd.DataFrame:

    """ Функция принимает на вход: датафрейм с транзакциями, название категории, опциональную дату.
    Если дата не передана, то берется текущая дата.
    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)."""

    df = get_dataframe()

    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)

    # Определяем, задана ли дата пользователем
    if date is None:
        now = datetime.now()
        formatted_date = now.strftime("%d.%m.%Y")
        date_obj = formatted_date
    else:
        date_obj = date

    # Преобразуем в datetime объект
    if isinstance(date_obj, str):
        date_for_filter = datetime.strptime(date_obj, "%d.%m.%Y")
    else:
        date_for_filter = date

    # Начало и конец месяца
    three_months_ago = date_for_filter - relativedelta(months=3)
    start_of_date = three_months_ago.strftime("%d.%m.%Y")
    end_of_date = date_for_filter.strftime("%d.%m.%Y")

    # print(f"Начало периода: {start_of_date}")
    # print(f"Конец периода: {end_of_date}")

    filtered_data = df[(df['Дата операции'] >= start_of_date) & (df['Дата операции'] <= end_of_date)]

    category_sum = filtered_data.loc[filtered_data['Категория'] == category, 'Сумма платежа'].abs().sum()

    return category_sum

print(spending_by_category("Фастфуд", "04.06.2021"))


