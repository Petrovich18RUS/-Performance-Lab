# Функция для чтения параметров эллипса из файла
def read_ellipse_file(filename):
    try:
        # Открываем файл для чтения
        with open(filename, 'r') as file:
            # Читаем все строки файла
            lines = file.readlines()

        # Первая строка - координаты центра эллипса
        center_line = lines[0].strip()  # Убираем лишние пробелы
        center_parts = center_line.split()  # Разделяем на две части
        center_x = float(center_parts[0])  # Первое число - x центра
        center_y = float(center_parts[1])  # Второе число - y центра

        # Вторая строка - радиусы эллипса
        radius_line = lines[1].strip()  # Убираем лишние пробелы
        radius_parts = radius_line.split()  # Разделяем на две части
        radius_x = float(radius_parts[0])  # Первое число - радиус по x
        radius_y = float(radius_parts[1])  # Второе число - радиус по y

        # Возвращаем все параметры эллипса
        return center_x, center_y, radius_x, radius_y

    except FileNotFoundError:
        # Если файл не найден
        print(f"ОШИБКА: Файл {filename} не найден!")
        return None
    except:
        # Если любая другая ошибка
        print(f"ОШИБКА: Не могу прочитать файл {filename}!")
        return None


# Функция для чтения точек из файла
def read_points_file(filename):
    points = []  # Список для хранения точек

    try:
        # Открываем файл для чтения
        with open(filename, 'r') as file:
            # Читаем файл построчно
            for line in file:
                line = line.strip()  # Убираем лишние пробелы
                if line == "":  # Пропускаем пустые строки
                    continue

                # Разделяем строку на две координаты
                coords = line.split()
                x = float(coords[0])  # Первое число - x координата
                y = float(coords[1])  # Второе число - y координата

                # Добавляем точку в список
                points.append((x, y))

        # Проверяем количество точек
        if len(points) < 1:
            print("ОШИБКА: В файле должно быть хотя бы 1 точка!")
            return None
        if len(points) > 100:
            print("ОШИБКА: В файле не может быть больше 100 точек!")
            return None

        return points

    except FileNotFoundError:
        # Если файл не найден
        print(f"ОШИБКА: Файл {filename} не найден!")
        return None
    except:
        # Если любая другая ошибка
        print(f"ОШИБКА: Не могу прочитать файл {filename}!")
        return None


# Функция для проверки положения точки относительно эллипса
def check_point_position(x, y, center_x, center_y, radius_x, radius_y):
    # Сдвигаем координаты так, чтобы центр эллипса был в (0,0)
    new_x = x - center_x
    new_y = y - center_y

    # Вычисляем значение по формуле эллипса
    # Формула: (x² / radius_x²) + (y² / radius_y²)
    part1 = (new_x * new_x) / (radius_x * radius_x)  # x² / rx²
    part2 = (new_y * new_y) / (radius_y * radius_y)  # y² / ry²
    value = part1 + part2  # Складываем две части

    # Проверяем где находится точка
    if abs(value - 1.0) < 0.0000000001:  # Если value почти равно 1
        return 0  # Точка на эллипсе
    elif value < 1.0:  # Если value меньше 1
        return 1  # Точка внутри эллипса
    else:  # Если value больше 1
        return 2  # Точка снаружи эллипса


# Главная функция программы
def main():
    print("=" * 40)
    print("ПРОГРАММА: ПОЛОЖЕНИЕ ТОЧЕК ОТНОСИТЕЛЬНО ЭЛЛИПСА")
    print("=" * 40)

    # Имена файлов (можно поменять если нужно)
    ellipse_filename = "ellipse.txt"  # Файл с параметрами эллипса
    points_filename = "points.txt"  # Файл с координатами точек

    print(f"Будем использовать файлы:")
    print(f"  ellipse.txt - параметры эллипса")
    print(f"  points.txt - координаты точек")
    print()

    # Читаем параметры эллипса
    print(f"Читаю параметры эллипса из файла: {ellipse_filename}")
    ellipse_params = read_ellipse_file(ellipse_filename)

    if ellipse_params is None:
        print("Не могу продолжить без параметров эллипса!")
        return

    center_x, center_y, radius_x, radius_y = ellipse_params
    print(f"✓ Центр эллипса: ({center_x}, {center_y})")
    print(f"✓ Радиусы: {radius_x} по X, {radius_y} по Y")
    print()

    # Читаем точки
    print(f"Читаю точки из файла: {points_filename}")
    points = read_points_file(points_filename)

    if points is None:
        print("Не могу продолжить без точек!")
        return

    print(f"✓ Найдено точек: {len(points)}")
    print()

    # Проверяем положение каждой точки
    print("РЕЗУЛЬТАТЫ:")
    print("-" * 20)

    for i, point in enumerate(points, 1):
        x, y = point
        # Проверяем положение точки
        result = check_point_position(x, y, center_x, center_y, radius_x, radius_y)
        # Выводим результат
        print(result)

    print("-" * 20)
    print("ГОТОВО!")


# Запускаем программу
if __name__ == "__main__":
    main()