import math
import json
import numpy as np
import matplotlib.pyplot as plt

# Загрузка данных из CSV файла
csv_file = "alt.csv"
heights_data = np.genfromtxt(csv_file, delimiter=',')
# Настройка опций печати для вывода полной матрицы

# Преобразование данных в матрицу размерностью 50x50
heights_matrix = heights_data.reshape((50, 50))


def within_radius(x1, y1, x2, y2, radius):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance <= radius


def filter_coordinates(matrix, object_x, object_y, object_radius, object_height):
    valid_coordinates = []
    rows = len(matrix)
    cols = len(matrix[0])

    for i in range(rows):
        for j in range(cols):
            if within_radius(object_x, object_y, i, j, object_radius) and matrix[i][j]:
                print(i, j)
                print(matrix[j][i])
                if matrix[j][i] <= object_height:
                    valid_coordinates.append((i, j))

    return valid_coordinates


object_x = 2
object_y = 2
object_radius = 1
object_height = 1

# Фильтрация координат
valid_coordinates = filter_coordinates(heights_matrix, object_x, object_y, object_radius, object_height)

print("Координаты, удовлетворяющие условиям:")
for coordinate in valid_coordinates:
    print(coordinate)
