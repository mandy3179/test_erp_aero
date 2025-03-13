def compare_pdf_structure(reference_data: dict[str, any], test_data: dict[str, any]) -> dict[str, str]:
    """Сравнивает структуру извлечённых данных из PDF с эталонной структурой.

    Функция проверяет соответствие текста, таблиц и изображений между эталонными и тестовыми данными.
    Возвращает словарь с описанием найденных несоответствий.

    Args:
        reference_data (dict[str, any]): Эталонные данные, содержащие тексты, таблицы и изображения.
        test_data (dict[str, any]): Тестовые данные, содержащие тексты, таблицы и изображения.

    Returns:
        dict[str, str]: Словарь, где ключи — это описание несоответствий (например, "text_line_1"),
                       а значения — строки с описанием различий (например, "Ожидалось: '...', Найдено: '...'").
                       Если несоответствий нет, возвращается пустой словарь.
    """
    mismatches: dict[str, str] = {}

    if reference_data.get("text") or test_data.get("text"):
        ref_text = "\n".join(reference_data.get("text", "")).split("\n")
        test_text = "\n".join(test_data.get("text", "")).split("\n")
        if len(ref_text) != len(test_text):
            mismatches["text_length"] = f"Несоответствие количества строк: {len(ref_text)} vs {len(test_text)}"
        else:
            for i, (ref_line, test_line) in enumerate(zip(ref_text, test_text)):
                if ref_line.strip() != test_line.strip():
                    mismatches[f"text_line_{i+1}"] = f"Ожидалось: '{ref_line}', Найдено: '{test_line}'"

    if reference_data.get("tables") or test_data.get("tables"):
        ref_tables = reference_data.get("tables", [])
        test_tables = test_data.get("tables", [])
        if len(ref_tables) != len(test_tables):
            mismatches["tables"] = "Несоответствие количества таблиц"
        else:
            for i, (ref_table, test_table) in enumerate(zip(ref_tables, test_tables)):
                if ref_table != test_table:
                    mismatches[f"table_{i+1}"] = "Несоответствие содержимого таблицы"

    if reference_data.get("images") or test_data.get("images"):
        ref_images = reference_data.get("images", [])
        test_images = test_data.get("images", [])
        if len(ref_images) != len(test_images):
            mismatches["images"] = "Несоответствие количества изображений"

    return mismatches
