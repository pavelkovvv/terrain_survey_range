import json
import numpy as np
import matplotlib.pyplot as plt

# Загрузка данных из CSV файла
csv_file = "alt.csv"
heights_data = np.genfromtxt(csv_file, delimiter=',')
# Настройка опций печати для вывода полной матрицы

# Преобразование данных в матрицу размерностью 50x50
heights_matrix = heights_data.reshape((50, 50))
# Сохранение матрицы в текстовый файл
output_file = "heights.txt"
np.savetxt(output_file, heights_matrix, fmt='%10.5f', delimiter='\t')
# Радиус обзора станции объективного контроля
radius = 1

# Высота станции
h = 1

# Местоположение станции
x, y = 2, 37

# Создание изолиний на основе данных
plt.contourf(heights_matrix, cmap='terrain')  # Используем цветовую карту 'terrain' для визуализации

# Добавление цветовой шкалы
plt.colorbar(label='Высота')

# Добавление заголовка и меток осей
plt.title('Визуализация матрицы высот')
plt.xlabel('Ширина')
plt.ylabel('Высота')

# Отображение графика
plt.show()


def generate_view_polygon(height_matrix, station_x, station_y, station_h, rds):
    # Определение координат центра станции
    center_x, center_y = station_x, station_y

    # Инициализация списка для точек полигона
    polygon_points = []
    print(len(height_matrix))
    print(len(height_matrix[0]))
    # Итерирование по каждой точке в матрице высот
    # for x in range(len(height_matrix)):
    #     for y in range(len(height_matrix[0])):
    #         print(height_matrix[x][y])
    #         # Проверка, находится ли точка в пределах радиуса обзора станции
    #         if (x - center_x) ** 2 + (y - center_y) ** 2 <= rds ** 2:
    #             # Получение высоты точки из матрицы высот
    #             height = height_matrix[x][y]
    #             print(height)
    #             # Проверка, достаточно ли высоко точка для обзора станцией
    #             if height <= station_h:
    #                 # Добавление координат точки в полигон
    #                 polygon_points.append([x, y])
    polygon_points.append([3, 3])
    polygon_points.append([3, 4])
    polygon_points.append([3, 5])
    polygon_points.append([3, 6])
    polygon_points.append([3, 7])
    polygon_points.append([3, 8])
    polygon_points.append([3, 9])
    # polygon_points.append([4, 4])
    # polygon_points.append([4, 5])
    # polygon_points.append([4, 6])
    # polygon_points.append([4, 7])
    # polygon_points.append([4, 8])
    # polygon_points.append([5, 5])
    # polygon_points.append([5, 6])
    # polygon_points.append([5, 7])
    # polygon_points.append([6, 6])
    # polygon_points.append([3, 4])
    # polygon_points.append([3, 5])
    # polygon_points.append([3, 6])
    # polygon_points.append([3, 7])
    # polygon_points.append([3, 8])
    # polygon_points.append([2, 5])
    # polygon_points.append([2, 6])
    # polygon_points.append([2, 7])
    # polygon_points.append([1, 6])


    # Формирование GeoJSON полигона
    geojson_polygon = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [polygon_points]
                },
                "properties": {
                    "station_x": station_x,
                    "station_y": station_y,
                    "station_h": station_h,
                    "radius": rds
                }
            }
        ]
    }

    return geojson_polygon


# Генерация полигона
polygon = generate_view_polygon(heights_matrix, x, y, h, radius)

# Сохранение полигона в файле GeoJSON
with open("view_polygon.geojson", "w") as file:
    json.dump(polygon, file, indent=2)

print("Полигон успешно сгенерирован и сохранен в файле view_polygon.geojson")
