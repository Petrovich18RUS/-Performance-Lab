import json
import sys
from typing import Dict, Any, List


class TestReportGenerator:
    # Класс для генерации отчета по тестам
    def __init__(self):
        self.values_dict = {}

    def load_json_file(self, file_path: str) -> Dict[str, Any]:
        #Загружаем JSON файл
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"Файл не найден: {file_path}")
        except json.JSONDecodeError:
            raise Exception(f"Некорректный JSON в файле: {file_path}")
        except Exception as e:
            raise Exception(f"Ошибка при чтении {file_path}: {str(e)}")

    def save_json_file(self, data: Dict[str, Any], file_path: str) -> None:
        #Сохраняем данные в JSON файл
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            print(f"✓ Отчет сохранен: {file_path}")
        except Exception as e:
            raise Exception(f"Ошибка при сохранении {file_path}: {str(e)}")

    def build_values_lookup(self, values_data: Dict[str, Any]) -> None:
        # Создаем словарь для быстрого поиска значений по ID теста
        if 'values' not in values_data:
            raise Exception("В файле values.json нет ключа 'values'")

        self.values_dict = {}
        for item in values_data['values']:
            if 'id' not in item or 'value' not in item:
                raise Exception("Некорректная структура в values.json")
            self.values_dict[item['id']] = item['value']

        print(f"Загружено {len(self.values_dict)} значений тестов")

    def fill_test_structure(self, tests_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        #Рекурсивно заполняем значения в структуре тестов
        filled_tests = []

        for test in tests_data:
            # Создаем копию теста
            filled_test = test.copy()

            # Заполняем значение, если ID есть в словаре
            test_id = filled_test.get('id')
            if test_id in self.values_dict:
                filled_test['value'] = self.values_dict[test_id]
                print(f"Заполнен тест ID {test_id}: {filled_test['value']}")
            else:
                print(f"⚠ Предупреждение: не найден результат для теста ID {test_id}")
                filled_test['value'] = ""  # или можно оставить пустым

            # Рекурсивно обрабатываем дочерние тесты
            if 'values' in filled_test and filled_test['values']:
                filled_test['values'] = self.fill_test_structure(filled_test['values'])

            filled_tests.append(filled_test)

        return filled_tests

    def generate_report(self, values_path: str, tests_path: str, report_path: str) -> None:
        # Основной метод для генерации отчета
        print("🚀 Запуск генерации отчета...")
        print(f"Файл значений: {values_path}")
        print(f"Файл тестов: {tests_path}")
        print(f"Выходной файл: {report_path}")
        print("-" * 50)

        # Загружаем данные
        print("📥 Загрузка данных...")
        values_data = self.load_json_file(values_path)
        tests_data = self.load_json_file(tests_path)

        # Проверяем структуру tests.json
        if 'tests' not in tests_data:
            raise Exception("В файле tests.json нет ключа 'tests'")

        # Строим словарь значений
        print("🔨 Построение словаря значений...")
        self.build_values_lookup(values_data)

        # Заполняем структуру тестов
        print("🎨 Заполнение структуры тестов...")
        filled_tests = self.fill_test_structure(tests_data['tests'])

        # Создаем отчет
        report_data = {'tests': filled_tests}

        # Сохраняем отчет
        print("💾 Сохранение отчета...")
        self.save_json_file(report_data, report_path)

        print("✅ Отчет успешно сгенерирован!")


def main():
    # Проверяем аргументы командной строки
    if len(sys.argv) != 4:
        print("❌ Ошибка: неверное количество аргументов!")
        print("\nИспользование:")
        print("  python test_report.py <values.json> <tests.json> <report.json>")
        print("\nПример:")
        print("  python test_report.py values.json tests.json report.json")
        print("\nАргументы:")
        print("  1. values.json - файл с результатами тестов")
        print("  2. tests.json  - файл со структурой тестов")
        print("  3. report.json - файл для сохранения отчета")
        sys.exit(1)

    # Извлекаем аргументы
    values_file = sys.argv[1]
    tests_file = sys.argv[2]
    report_file = sys.argv[3]

    # Создаем генератор и запускаем
    generator = TestReportGenerator()

    try:
        generator.generate_report(values_file, tests_file, report_file)
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()