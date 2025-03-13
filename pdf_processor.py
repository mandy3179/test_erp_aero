import pdfplumber
from collections import defaultdict


def extract_pdf_data(pdf_path: str) -> dict[str, any]:
    """Извлекает текст, таблицы и изображения из PDF-файла.

    Функция проходит по каждой странице PDF-файла и извлекает:
    - Текст (если он присутствует на странице).
    - Таблицы (если они присутствуют на странице).
    - Изображения (если они присутствуют на странице).

    Метаданные PDF (например, автор, дата создания) игнорируются.

    Args:
        pdf_path (str): Путь к PDF-файлу, из которого нужно извлечь данные.

    Returns:
        dict[str, any]: Словарь, содержащий извлечённые данные. Ключи:
                       - "text": список строк с текстом, извлечённым из каждой страницы.
                       - "tables": список таблиц, где каждая таблица представлена как список строк.
                       - "images": список изображений, извлечённых из страниц.
                       Если какой-то тип данных отсутствует, соответствующего ключа не будет в словаре.
    """
    data: dict[str, list[any]] = defaultdict(list)
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text: str = page.extract_text()
            if text:
                data["text"].append(text)

            tables: list[list[str]] = page.extract_tables()
            if tables:
                data["tables"].extend(tables)

            for img in page.images:
                data["images"].append(img)

    return {key: value if isinstance(value, list) else value for key, value in data.items()}
