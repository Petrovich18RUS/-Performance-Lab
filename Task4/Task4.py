import sys


def read_numbers_from_file(filename):
    #Читаем числа из файла
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            numbers = []
            for line in file:
                line = line.strip()
                if line:  # Пропускаем пустые строки
                    numbers.append(int(line))
            return numbers
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден!")
        return None
    except ValueError:
        print(f"Ошибка: в файле содержатся некорректные числа!")
        return None


def calculate_min_moves(numbers):
    #Вычисляем минимальное количество ходов для приведения всех чисел к одному значению
    if not numbers:
        return 0

    # Сортируем массив для нахождения медианы
    sorted_nums = sorted(numbers)

    # Для нечетного количества - берем средний элемент
    # Для четного - можно брать любой из двух средних, результат будет одинаков
    n = len(sorted_nums)
    median = sorted_nums[n // 2]

    # Вычисляем общее количество ходов
    total_moves = 0
    for num in numbers:
        total_moves += abs(num - median)

    return total_moves


def main():
    #Основная функция программы
    filename = "numbers.txt"
    print(f"Читаем числа из файла: {filename}")

    # Читаем числа из файла
    numbers = read_numbers_from_file(filename)
    if numbers is None:
        return

    # Проверяем что массив не пустой
    if len(numbers) == 0:
        print("Ошибка: файл пустой!")
        return

    print(f"Прочитано чисел: {len(numbers)}")
    print(f"Числа: {numbers}")

    # Вычисляем минимальное количество ходов
    min_moves = calculate_min_moves(numbers)

    print(f"Минимальное количество ходов: {min_moves}")

    # Проверяем ограничение в 20 ходов
    if min_moves <= 20:
        print(f"Ответ: {min_moves}")
    else:
        print("20 ходов недостаточно для приведения всех элементов массива к одному числу")


if __name__ == "__main__":
    main()