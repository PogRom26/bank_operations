import pytest
from unittest.mock import patch
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


def test_process_bank_search_basic_case(mock_transactions):
    """Тест базового случая поиска по слову"""
    with patch('src.services.data_frame_filtered_by_date', return_value=mock_transactions):
        result = process_bank_search("01.07.2021", "колхоз")
        data = json.loads(result)

        assert len(data) == 2
        assert all(('колхоз' in item['Описание'].lower() or
                    'колхоз' in item['Категория'].lower())
                   for item in data)


def test_process_bank_search_empty_result(mock_transactions):
    """Тест случая без результатов поиска"""
    with patch('src.services.data_frame_filtered_by_date', return_value=mock_transactions):
        result = process_bank_search("01.07.2021", "несуществующееслово")
        assert json.loads(result) == []


def test_process_bank_search_case_insensitive(mock_transactions):
    """Тест регистронезависимого поиска"""
    with patch('src.services.data_frame_filtered_by_date', return_value=mock_transactions):
        result = process_bank_search("01.07.2021", "КОЛХОЗ")
        data = json.loads(result)
        assert len(data) == 2


def test_process_bank_search_empty_search_word(mock_transactions):
    """Тест пустого поискового запроса"""
    with patch('src.services.data_frame_filtered_by_date', return_value=mock_transactions):
        result = process_bank_search("01.07.2021", "")
        data = json.loads(result)
        assert len(data) == 3  # Должны вернуть все записи


def test_process_bank_search_special_characters():
    """Тест поиска с специальными символами"""
    test_data = pd.DataFrame({
        'Дата операции': ['01.07.2021'],
        'Описание': ['Покупка в "Колхоз" №3'],
        'Категория': ['Продукты'],
        'Сумма': [-1000]
    })

    with patch('src.services.data_frame_filtered_by_date', return_value=test_data):
        result = process_bank_search("01.07.2021", "колхоз")
        data = json.loads(result)
        assert len(data) == 1


def test_process_bank_search_json_structure(mock_transactions):
    """Тест структуры выходного JSON"""
    with patch('src.services.data_frame_filtered_by_date', return_value=mock_transactions):
        result = process_bank_search("01.07.2021", "колхоз")
        data = json.loads(result)

        assert isinstance(data, list)
        assert all(isinstance(item, dict) for item in data)
        assert all(key in item for item in data
                   for key in ['Дата операции', 'Описание', 'Категория', 'Сумма'])


def test_process_bank_search_date_filtering():
    """Тест фильтрации по дате (мок функции data_frame_filtered_by_date)"""
    test_data = pd.DataFrame({
        'Дата операции': ['01.06.2021', '01.07.2021', '01.08.2021'],
        'Описание': ['Колхоз июнь', 'Колхоз июль', 'Колхоз август'],
        'Категория': ['Продукты', 'Продукты', 'Продукты'],
        'Сумма': [-500, -600, -700]
    })

    with patch('src.services.data_frame_filtered_by_date', return_value=test_data) as mock_filter:
        process_bank_search("01.07.2021", "колхоз")

        # Проверяем, что функция фильтрации вызвана
        mock_filter.assert_called_once()


@pytest.mark.parametrize("search_word, expected_count", [
    ("колхоз", 2),
    ("кафе", 1),
    ("перевод", 1),
    ("", 3)  # Пустой запрос должен вернуть все
])
def test_parametrized_search(search_word, expected_count, mock_transactions):
    """Параметризованный тест с разными поисковыми запросами"""
    with patch('src.services.data_frame_filtered_by_date', return_value=mock_transactions):
        result = process_bank_search("01.07.2021", search_word)
        assert len(json.loads(result)) == expected_count