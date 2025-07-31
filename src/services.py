import pandas as pd
from src.utils import data_frame_filtered_by_date


def process_bank_search(user_date: str = "04.09.2021", search_word: str = "") -> list[dict]:
    """Пользователь передает строку для поиска, возвращается JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории."""

    def contains_word(row, word):
        """Проверяет, содержится ли слово в строке"""
        return any(str(cell).lower().find(word.lower()) != -1
                   for cell in row if pd.notna(cell))

    filtered_data = data_frame_filtered_by_date()

    mask = (
            filtered_data['Описание'].astype(str).str.contains(search_word, case=False, na=False) |
            filtered_data['Категория'].astype(str).str.contains(search_word, case=False, na=False)
    )

    results = filtered_data[mask]
    json_data = results.to_json(orient='records', force_ascii=False, indent=2)

    return json_data

print(process_bank_search("01.07.2021", "колхоз"))