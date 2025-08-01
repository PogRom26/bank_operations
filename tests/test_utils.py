import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytest

# Импортируем нашу функцию
from src.utils import greeting, get_dataframe, data_frame_filtered_by_date

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

 # Проверка вывода датафрейма
def test_get_dataframe():
    x = get_dataframe()
    assert type(x) == pd.DataFrame


# Проверка обработки некорректной даты
def test_invalid_user_input():
    with pytest.raises(ValueError):
        data_frame_filtered_by_date("invalid_date_format")

# Проверка расчета кэшбэка
def test_cashback_calculation():
    result_df = data_frame_filtered_by_date("01.09.2021")
    cashbacks = result_df['Сумма кэшбэка'].values.tolist()
    expected_cashbacks = [round(amount / 100, 2) for amount in [1000, 2000]]
    assert cashbacks == expected_cashbacks, "Кэшбек рассчитан неверно"

# Пустой датафрейм
def test_data_frame_filtered_by_date():
    x = data_frame_filtered_by_date()
    assert type(x) == pd.DataFrame


import pytest
import pandas as pd
from unittest.mock import patch
import json

# Импортируем функцию для тестирования
from src.utils import top_transactions


# Фикстура для тестового DataFrame
@pytest.fixture
def sample_dataframe():
    data = {
        'Дата платежа': ['01.07.2021', '02.07.2021', '03.07.2021', '04.07.2021', '05.07.2021', '06.07.2021'],
        'Сумма платежа': [1000, 500, 2000, 300, 1500, 100],
        'Категория': ['Продукты', 'Транспорт', 'Рестораны', 'Продукты', 'Транспорт', 'Развлечения'],
        'Описание': ['Покупка в супермаркете', 'Билет на автобус', 'Ужин в ресторане', 'Молоко', 'Такси', 'Кино']
    }
    return pd.DataFrame(data)


# Тест 1: Проверка выбора топ-5 транзакций
@patch('src.utils.data_frame_filtered_by_date')
def test_top_transactions_top_5(mock_data_frame_filtered_by_date, sample_dataframe):
    mock_data_frame_filtered_by_date.return_value = sample_dataframe
    result = top_transactions("01.07.2021")

    expected = {
        'top_transactions': [
            {'date': '03.07.2021', 'amount': 2000, 'category': 'Рестораны', 'description': 'Ужин в ресторане'},
            {'date': '05.07.2021', 'amount': 1500, 'category': 'Транспорт', 'description': 'Такси'},
            {'date': '01.07.2021', 'amount': 1000, 'category': 'Продукты', 'description': 'Покупка в супермаркете'},
            {'date': '02.07.2021', 'amount': 500, 'category': 'Транспорт', 'description': 'Билет на автобус'},
            {'date': '04.07.2021', 'amount': 300, 'category': 'Продукты', 'description': 'Молоко'}
        ]
    }

    assert result == expected
    assert len(result['top_transactions']) == 5


# Тест 3: Проверка случая с менее чем 5 транзакциями
@patch('src.utils.data_frame_filtered_by_date')
def test_top_transactions_less_than_5(mock_data_frame_filtered_by_date):
    small_df = pd.DataFrame({
        'Дата платежа': ['01.07.2021', '02.07.2021'],
        'Сумма платежа': [1000, 500],
        'Категория': ['Продукты', 'Транспорт'],
        'Описание': ['Покупка в супермаркете', 'Билет на автобус']
    })
    mock_data_frame_filtered_by_date.return_value = small_df
    result = top_transactions("01.07.2021")

    expected = {
        'top_transactions': [
            {'date': '01.07.2021', 'amount': 1000, 'category': 'Продукты', 'description': 'Покупка в супермаркете'},
            {'date': '02.07.2021', 'amount': 500, 'category': 'Транспорт', 'description': 'Билет на автобус'}
        ]
    }

    assert result == expected
    assert len(result['top_transactions']) == 2


# Тест 4: Проверка преобразования ключей
@patch('src.utils.data_frame_filtered_by_date')
def test_top_transactions_key_mapping(mock_data_frame_filtered_by_date, sample_dataframe):
    mock_data_frame_filtered_by_date.return_value = sample_dataframe
    result = top_transactions("01.07.2021")

    # Проверяем, что все ключи преобразованы в английские
    for transaction in result['top_transactions']:
        assert set(transaction.keys()) == {'date', 'amount', 'category', 'description'}
        assert 'Дата платежа' not in transaction
        assert 'Сумма платежа' not in transaction
        assert 'Категория' not in transaction
        assert 'Описание' not in transaction


# Тест 5: Проверка формата возвращаемого JSON
@patch('src.utils.data_frame_filtered_by_date')
def test_top_transactions_json_format(mock_data_frame_filtered_by_date, sample_dataframe):
    mock_data_frame_filtered_by_date.return_value = sample_dataframe
    result = top_transactions("01.07.2021")

    # Проверяем структуру
    assert isinstance(result, dict)
    assert 'top_transactions' in result
    assert isinstance(result['top_transactions'], list)
    assert len(result['top_transactions']) <= 5
    if result['top_transactions']:
        assert all(isinstance(t, dict) for t in result['top_transactions'])
        assert all('date' in t and 'amount' in t and 'category' in t and 'description' in t
                   for t in result['top_transactions'])


# Тест 6: Проверка игнорирования user_date
@patch('src.utils.data_frame_filtered_by_date')
def test_top_transactions_date_ignored(mock_data_frame_filtered_by_date, sample_dataframe):
    mock_data_frame_filtered_by_date.return_value = sample_dataframe
    result1 = top_transactions("01.07.2021")
    result2 = top_transactions("01.08.2021")

    # Поскольку user_date не используется в функции, результаты должны быть одинаковыми
    assert result1 == result2


# Тест 7: Проверка вызова data_frame_filtered_by_date
@patch('src.utils.data_frame_filtered_by_date')
def test_top_transactions_calls_data_frame_filtered_by_date(mock_data_frame_filtered_by_date, sample_dataframe):
    mock_data_frame_filtered_by_date.return_value = sample_dataframe
    top_transactions("01.07.2021")

    # Проверяем, что функция data_frame_filtered_by_date была вызвана один раз
    mock_data_frame_filtered_by_date.assert_called_once()

