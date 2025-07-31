import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from src.reports import spending_by_category


@pytest.fixture
def mock_transactions():
    """Фикстура с тестовыми данными транзакций"""
    return pd.DataFrame({
        'Дата операции': ['01.01.2023', '15.02.2023', '01.03.2023', '10.04.2023'],
        'Категория': ['Еда', 'Транспорт', 'Еда', 'Еда'],
        'Сумма платежа': [-1500, -500, -2000, -1200]
    })


def test_spending_by_category_basic(mock_transactions):
    """Тест базового случая - категория существует"""
    with patch('your_module.get_dataframe', return_value=mock_transactions):
        result = spending_by_category('Еда', '01.05.2023')
        assert result == 4700  # 1500 + 2000 + 1200 (абсолютные значения)


def test_spending_by_category_no_data(mock_transactions):
    """Тест для категории без данных"""
    with patch('your_module.get_dataframe', return_value=mock_transactions):
        result = spending_by_category('Развлечения', '01.05.2023')
        assert result == 0


def test_spending_by_category_current_date():
    """Тест с текущей датой (автоматическое определение)"""
    test_data = pd.DataFrame({
        'Дата операции': [(datetime.now() - relativedelta(months=1)).strftime("%d.%m.%Y")],
        'Категория': ['Еда'],
        'Сумма платежа': [-2500]
    })

    with patch('your_module.get_dataframe', return_value=test_data), \
            patch('your_module.datetime') as mock_datetime:
        # Мокаем текущую дату
        mock_now = datetime(2023, 5, 15)
        mock_datetime.now.return_value = mock_now

        result = spending_by_category('Еда')
        assert result == 2500


def test_spending_by_category_date_parsing():
    """Тест корректности парсинга даты"""
    test_data = pd.DataFrame({
        'Дата операции': ['01.04.2023'],
        'Категория': ['Еда'],
        'Сумма платежа': [-1000]
    })

    with patch('your_module.get_dataframe', return_value=test_data):
        result = spending_by_category('Еда', '15.05.2023')
        assert result == 1000


def test_spending_by_category_edge_cases():
    """Тест граничных случаев"""
    test_data = pd.DataFrame({
        'Дата операции': ['31.12.2022', '01.01.2023', '31.03.2023'],
        'Категория': ['Еда', 'Еда', 'Еда'],
        'Сумма платежа': [-1000, -2000, -3000]
    })

    with patch('your_module.get_dataframe', return_value=test_data):
        # Проверка перехода через год
        result = spending_by_category('Еда', '30.04.2023')
        assert result == 6000  # 1000 + 2000 + 3000


def test_spending_by_category_mocked_datetime():
    """Тест с моком datetime для фиксированной даты"""
    test_data = pd.DataFrame({
        'Дата операции': ['01.02.2023'],
        'Категория': ['Еда'],
        'Сумма платежа': [-1500]
    })

    with patch('your_module.get_dataframe', return_value=test_data), \
            patch('your_module.datetime') as mock_datetime:
        # Фиксируем дату для теста
        mock_now = datetime(2023, 5, 1)
        mock_datetime.now.return_value = mock_now
        mock_datetime.strptime.side_effect = lambda *args, **kw: datetime.strptime(*args, **kw)

        result = spending_by_category('Еда')
        assert result == 1500


def test_spending_by_category_empty_df():
    """Тест с пустым DataFrame"""
    with patch('your_module.get_dataframe', return_value=pd.DataFrame()):
        result = spending_by_category('Еда', '01.05.2023')
        assert result == 0