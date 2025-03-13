from pdf_processor import extract_pdf_data
from structure_checker import compare_pdf_structure
import sys


def main(reference_pdf: str, test_pdf: str):
    print(f"Обработка эталонного PDF: {reference_pdf}")
    reference_data = extract_pdf_data(reference_pdf)
    
    print(f"Обработка тестового PDF: {test_pdf}")
    test_data = extract_pdf_data(test_pdf)
    
    print("Сравнение структуры PDF...")
    mismatches = compare_pdf_structure(reference_data, test_data)
    
    if mismatches:
        print("Найдены различия:")
        for key, value in mismatches.items():
            print(f"- {key}: {value}")
    else:
        print("Тестовый PDF соответствует структуре эталона.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Используйте: python main.py <эталонный_PDF> <тестовый_PDF>")
        sys.exit(1)
    
    reference_pdf_path = sys.argv[1]
    test_pdf_path = sys.argv[2]
    main(reference_pdf_path, test_pdf_path)
