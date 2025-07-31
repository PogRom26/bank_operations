import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import json
from src.services import process_bank_search


@pytest.fixture
def mock_transactions():
    """Фикстура с тестовыми данными транзакций"""
    return pd.DataFrame({
        'Дата операции': ['01.07.2021', '15.07.2021', '01.08.2021'],
        'Описание': ['Покупка в Колхозе', 'Оплата кафе', 'Перевод в колхоз'],
        'Категория': ['Продукты', 'Рестораны', 'Переводы'],
        'Сумма': [-1000, -500, -2000]
    })


def test_process_bank_search_basic(mock_transactions):
    """Тест базового случая - поиск по слову"""
    with patch('src.main.data_frame_filtered_by_date', return_value=mock_transactions):
        result = process_bank_search("01.07.2021", "колхоз")
        data = json.loads(result)

        assert len(data) == 2
        assert all(('колхоз' in item['Описание'].lower()) or
                   ('колхоз' in item['Категория'].lower())
                   for item in data)


def test_process_bank_search_empty_result(mock_transactions):
    """Тест случая без результатов"""
    with patch('src.main.data_frame_filtered_by_date', return_value=mock_transactions):
        result = process_bank_search("01.07.2021", "несуществующееслово")
        assert json.loads(result) == []


def test_process_bank_search_case_insensitive(mock_transactions):
    """Тест регистронезависимого поиска"""
    with patch('src.main.data_frame_filtered_by_date', return_value=mock_transactions):
        result = process_bank_search("01.07.2021", "КОЛХОЗ")
        data = json.loads(result)
        assert len(data) == 2


def test_process_bank_search_date_filtering():
    """Тест фильтрации по дате"""
    test_data = pd.DataFrame({
        'Дата операции': ['01.06.2021', '01.07.2021', '01.08.2021'],
        'Описание': ['Колхоз июнь', 'Колхоз июль', 'Колхоз август'],
        'Категория': ['Продукты', 'Продукты', 'Продукты'],
        'Сумма': [-500, -600, -700]
    })

    with patch('src.main.data_frame_filtered_by_date', return_value=test_data):
        # Должны найти только записи начиная с 01.07.2021
        result = process_bank_search("01.07.2021", "колхоз")
        data = json.loads(result)
        assert len(data) == 2
        assert 'июль' in data[0]['Описание']
        assert 'август' in data[1]['Описание']


def test_process_bank_search_empty_input():
    """Тест пустого поискового запроса"""
    test_data = pd.DataFrame({
        'Дата операции': ['01.07.2021'],
        'Описание': ['Покупка в магазине'],
        'Категория': ['Продукты'],
        'Сумма': [-1000]
    })

    with patch('src.main.data_frame_filtered_by_date', return_value=test_data):
        result = process_bank_search("01.07.2021", "")
        data = json.loads(result)
        assert len(data) == 1  # Должны вернуть все записи


def test_process_bank_search_special_chars():
    """Тест поиска с специальными символами"""
    test_data = pd.DataFrame({
        'Дата операции': ['01.07.2021'],
        'Описание': ['Покупка в "Колхоз" №3'],
        'Категория': ['Продукты'],
        'Сумма': [-1000]
    })

    with patch('src.main.data_frame_filtered_by_date', return_value=test_data):
        result = process_bank_search("01.07.2021", "колхоз")
        data = json.loads(result)
        assert len(data) == 1


def test_process_bank_search_json_structure():
    """Тест структуры выходного JSON"""
    test_data = pd.DataFrame({
        'Дата операции': ['01.07.2021'],
        'Описание': ['Колхоз'],
        'Категория': ['Продукты'],
        'Сумма': [-1000]
    })

    with patch('src.main.data_frame_filtered_by_date', return_value=test_data):
        result = process_bank_search("01.07.2021", "колхоз")
        data = json.loads(result)

        assert isinstance(data, list)
        assert all(isinstance(item, dict) for item in data)
        assert all(key in item for item in data
                   for key in ['Дата операции', 'Описание', 'Категория', 'Сумма'])