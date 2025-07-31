import pytest
from datetime import datetime

# Импортируем нашу функцию
from src.utils import greeting  # your_module — название модуля, где находится функция greeting

# Тест-кейсы для утреннего времени (6–12 часов)
@pytest.mark.parametrize(
    "hour,expected_greeting",
    [(7, "Доброе утро!"), (11, "Доброе утро!")]
)
def test_morning_greeting(hour, expected_greeting):
    date = datetime(year=2023, month=10, day=1, hour=hour)
    result = greeting(date)
    assert result == {"greeting": expected_greeting}, f"Expected greeting '{expected_greeting}'"

# Тест-кейсы для дневного времени (12–18 часов)
@pytest.mark.parametrize(
    "hour,expected_greeting",
    [(13, "Добрый день!"), (17, "Добрый день!")]
)
def test_day_greeting(hour, expected_greeting):
    date = datetime(year=2023, month=10, day=1, hour=hour)
    result = greeting(date)
    assert result == {"greeting": expected_greeting}, f"Expected greeting '{expected_greeting}' at {hour}:00 but got {result}"

# Тест-кейсы для вечернего времени (18–24 часа)
@pytest.mark.parametrize(
    "hour,expected_greeting",
    [(19, "Добрый вечер!"), (23, "Добрый вечер!")]
)
def test_evening_greeting(hour, expected_greeting):
    date = datetime(year=2023, month=10, day=1, hour=hour)
    result = greeting(date)
    assert result == {"greeting": expected_greeting}, f"Expected greeting '{expected_greeting}' at {hour}:00 but got {result}"

# Тест-кейсы для ночного времени (0–6 часов)
@pytest.mark.parametrize(
    "hour,expected_greeting",
    [(0, "Доброй ночи!"), (5, "Доброй ночи!")]
)
def test_night_greeting(hour, expected_greeting):
    date = datetime(year=2023, month=10, day=1, hour=hour)
    result = greeting(date)
    assert result == {"greeting": expected_greeting}, f"Expected greeting '{expected_greeting}' at {hour}:00 but got {result}"

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytest
from src.utils import data_frame_filtered_by_date, get_dataframe  # импортируйте вашу функцию из нужного модуля

# Тестовые данные
@pytest.fixture
def dataframe_fixture():
    data = {
        'Дата операции': ['01.09.2021', '15.09.2021', '01.10.2021'],
        'Сумма платежа': [1000, 2000, 3000],
    }
    df = pd.DataFrame(data)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)
    return df

# Модификация базовой функции get_dataframe(), чтобы возвращалась фиктивная таблица
@pytest.fixture(autouse=True)
def mock_get_dataframe(monkeypatch, dataframe_fixture):
    def mocked_get_dataframe():
        return dataframe_fixture
    monkeypatch.setattr('src.utils.get_dataframe', mocked_get_dataframe)

# Тест 1: Фильтрация по правильному месяцу
def test_filter_correct_month():
    result_df = data_frame_filtered_by_date("09.2021")
    expected_rows = ['01.09.2021', '15.09.2021']
    actual_dates = result_df['Дата операции'].dt.strftime("%d.%m.%Y").tolist()
    assert actual_dates == expected_rows, "Даты неправильно фильтруются"

# Тест 2: Фильтрация по другому месяцу
def test_filter_different_month():
    result_df = data_frame_filtered_by_date("10.2021")
    expected_rows = ['01.10.2021']
    actual_dates = result_df['Дата операции'].dt.strftime("%d.%m.%Y").tolist()
    assert actual_dates == expected_rows, "Неправильно выбраны даты другого месяца"

# Тест 3: Проверка обработки некорректной даты
def test_invalid_user_input():
    with pytest.raises(ValueError):
        data_frame_filtered_by_date("invalid_date_format")

# Тест 4: Проверка расчета кэшбэка
def test_cashback_calculation():
    result_df = data_frame_filtered_by_date("09.2021")
    cashbacks = result_df['Сумма кэшбэка'].values.tolist()
    expected_cashbacks = [round(amount / 100, 2) for amount in [1000, 2000]]
    assert cashbacks == expected_cashbacks, "Кэшбек рассчитан неверно"

# Тест 5: Пустой датафрейм
def test_empty_dataframe():
    empty_df = pd.DataFrame(columns=['Дата операции'])
    monkeypatch.setattr('your_module.get_dataframe', lambda : empty_df)
    result_df = data_frame_filtered_by_date("09.2021")
    assert result_df.empty, "Результат не пустой, хотя исходный датафрейм пустой"