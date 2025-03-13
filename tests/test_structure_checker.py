import pytest
from pdf_processor import extract_pdf_data
from structure_checker import compare_pdf_structure


@pytest.fixture
def sample_pdf_data():
    """Фикстура для предоставления эталонных данных, извлеченных из PDF."""
    return extract_pdf_data("data/reference.pdf")

def test_extract_text(sample_pdf_data):
    """Тестирует корректность извлечения текста из PDF."""
    extracted_text = "\n".join(sample_pdf_data.get("text", []))
    assert "GRIFFON AVIATION SERVICES LLC" in extracted_text
    assert "Qty: 1" in extracted_text

def test_extract_metadata(sample_pdf_data):
    """Тестирует корректность извлечения метаданных из PDF."""
    assert isinstance(sample_pdf_data.get("metadata", {}), dict)

def test_extract_tables(sample_pdf_data):
    """Тестирует корректность извлечения таблиц из PDF."""
    assert isinstance(sample_pdf_data.get("tables", []), list)

def test_extract_images(sample_pdf_data):
    """Тестирует корректность извлечения изображений из PDF."""
    assert isinstance(sample_pdf_data.get("images", []), list)

def test_identical_pdfs():
    """Тест сравнивает два идентичных PDF-файла, ожидая отсутствие различий."""
    reference_data = {
        "text": "Sample text\nSecond line",
        "tables": [
            [
                ['Header1', 'Header2'],
                ['Data1', 'Data2']
            ]
        ],
        "images": ["image1.png"]
    }
    test_data = reference_data.copy()
    mismatches = compare_pdf_structure(reference_data, test_data)
    assert mismatches == {}

def test_text_mismatch():
    """Тест проверяет, что изменения в тексте фиксируются как несоответствие."""
    reference_data = {"text": "Sample text\nSecond line"}
    test_data = {"text": "Sample text\nModified line"}
    mismatches = compare_pdf_structure(reference_data, test_data)
    assert "text_length" in mismatches

def test_table_mismatch():
    """Тест сравнивает PDF с измененной таблицей, ожидая обнаружение различий."""
    reference_data = extract_pdf_data("data/reference.pdf")
    altered_data = reference_data.copy()
    altered_data["tables"] = [[['Header2', 'Header3']]]  # Измененная таблица
    mismatches = compare_pdf_structure(reference_data, altered_data)
    assert any(key.startswith("table") for key in mismatches)

def test_missing_images():
    """Тест проверяет, что отсутствие изображений фиксируется как ошибка."""
    reference_data = {"images": ["image1.png"]}
    test_data = {"images": []}
    mismatches = compare_pdf_structure(reference_data, test_data)
    assert "images" in mismatches

def test_extra_text():
    """Тест проверяет, что добавленный текст фиксируется как несоответствие."""
    reference_data = {"text": "Sample text"}
    test_data = {"text": "Sample text\nExtra line"}
    mismatches = compare_pdf_structure(reference_data, test_data)
    assert "text_length" in mismatches

def test_empty_text():
    """Тест проверяет обработку случая, когда текст отсутствует."""
    reference_data = {"text": ""}
    test_data = {"text": ""}
    mismatches = compare_pdf_structure(reference_data, test_data)
    assert mismatches == {}

def test_missing_text_in_test_data():
    """Тест проверяет ситуацию, когда в тестируемом файле отсутствует текст."""
    reference_data = {"text": "Sample text"}
    test_data = {"text": ""}
    mismatches = compare_pdf_structure(reference_data, test_data)
    assert "text_length" in mismatches

def test_multiple_mismatches():
    """Тест проверяет обнаружение нескольких несоответствий одновременно."""
    reference_data = {
        "text": "Line1\nLine2",
        "tables": [[['A', 'B'], ['C', 'D']]],
        "images": ["img1.png"]
    }
    test_data = {
        "text": "Line1\nDifferent line",
        "tables": [[['A', 'B']]],
        "images": []
    }
    mismatches = compare_pdf_structure(reference_data, test_data)
    assert any(key.startswith("text_line") for key in mismatches) or "text_length" in mismatches
    assert any(key.startswith("table") for key in mismatches) or "tables" in mismatches
    assert "images" in mismatches
