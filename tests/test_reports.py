import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from typing import Optional
from src.reports import spending_by_category  # Импорт тестируемой функции


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми данными транзакций"""
    return pd.DataFrame({
        'Дата операции': ['01.03.2021', '15.04.2021', '01.05.2021', '10.06.2021', '05.07.2021'],
        'Категория': ['Фастфуд', 'Транспорт', 'Фастфуд', 'Фастфуд', 'Кафе'],
        'Сумма платежа': [-500, -200, -800, -300, -150]
    })


def test_spending_by_category_basic(sample_transactions):
    """Тест базового случая с передачей даты"""
    result = spending_by_category(sample_transactions, "Фастфуд", "04.07.2021")
    assert float(result) == 1100  # 500 (март) + 800 (май)


def test_spending_by_category_current_date(sample_transactions):
    """Тест с автоматическим определением текущей даты"""
    with patch('src.reports.datetime') as mock_datetime:
        # Мокаем текущую дату
        mock_now = datetime(2021, 6, 4)
        mock_datetime.now.return_value = mock_now
        mock_datetime.strptime.side_effect = lambda *args, **kw: datetime.strptime(*args, **kw)

        result = spending_by_category(sample_transactions, "Фастфуд")
        assert float(result) == 800


def test_spending_by_category_no_matches(sample_transactions):
    """Тест для категории без совпадений"""
    result = spending_by_category(sample_transactions, "Такси", "04.06.2021")
    assert result == 0


def test_spending_by_category_date_filtering(sample_transactions):
    """Тест корректности фильтрации по дате"""
    result = spending_by_category(sample_transactions, "Фастфуд", "15.04.2021")
    assert result == 500  # Только март


def test_spending_by_category_edge_case_year_change():
    """Тест перехода через год"""
    special_data = pd.DataFrame({
        'Дата операции': ['15.12.2020', '10.01.2021', '20.02.2021'],
        'Категория': ['Фастфуд', 'Фастфуд', 'Фастфуд'],
        'Сумма платежа': [-600, -700, -800]
    })

    result = spending_by_category(special_data, "Фастфуд", "28.02.2021")
    assert result == 2100  # Декабрь + Январь + Февраль


def test_spending_by_category_absolute_values():
    """Тест корректности работы с абсолютными значениями"""
    test_data = pd.DataFrame({
        'Дата операции': ['01.05.2021'],
        'Категория': ['Фастфуд'],
        'Сумма платежа': [-1500]
    })

    result = spending_by_category(test_data, "Фастфуд", "30.05.2021")
    assert result == 1500  # Должно быть положительное число
