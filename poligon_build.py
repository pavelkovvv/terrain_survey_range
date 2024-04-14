import math
import json
import numpy as np


class PolygonBuild:
    """
    Позволяет создавать объекты для построения полигонов на основе
    заданных параметров.
    """

    def __init__(
            self,
            csv_file_path: str,
            matrix_len_x: int,
            matrix_len_y: int,
            obj_x: int,
            obj_y: int,
            obj_radius: int,
            obj_height: int,
            geojson_file_path: str,
    ):
        self.csv_file_path = csv_file_path
        self.matrix_len_x = matrix_len_x
        self.matrix_len_y = matrix_len_y
        self.obj_x = obj_x
        self.obj_y = obj_y
        self.obj_radius = obj_radius
        self.obj_height = obj_height
        self.geojson_file_path = geojson_file_path

    def converting_to_matrix(self) -> np.ndarray:
        """Преобразует CSV-файл с высотами в матрицу определенного размера."""

        heights_data = np.genfromtxt(self.csv_file_path, delimiter=',')
        heights_matrix = heights_data.reshape((self.matrix_len_x, self.matrix_len_y))

        return heights_matrix

    def within_radius(self, x: int, y: int) -> bool:
        """Проверяет, находится ли точка в пределах радиуса от центра станции."""

        distance = math.sqrt((self.obj_x - x) ** 2 + (self.obj_y - y) ** 2)

        return distance <= self.obj_radius

    def filter_coordinates(self) -> list:
        """
        Возвращает координаты, которые удовлетворяют условиям:
        1) Попадают в радиус видимости объекта;
        2) Меньше или равны высоте станции.
        """

        valid_coordinates = list()
        heights_matrix = self.converting_to_matrix()
        rows = len(heights_matrix)
        cols = len(heights_matrix[0])

        for i in range(rows):
            for j in range(cols):
                if self.within_radius(i, j) and heights_matrix[i][j]:
                    if heights_matrix[j][i] <= self.obj_height:
                        valid_coordinates.append([i, j])

        return valid_coordinates

    def build_polygon(self) -> list:
        """Строит и возвращает итоговый полигон на основе отфильтрованных координат."""

        polygon = list()
        central_point = [self.obj_x, self.obj_y]
        valid_coords = self.filter_coordinates()

        # Создание словаря для группировки координат по значению x
        grouped_coordinates = dict()

        # Группируем координаты по значению x
        for x, y in valid_coords:
            if x not in grouped_coordinates:
                grouped_coordinates[x] = []
            grouped_coordinates[x].append([x, y])

        # Получим первую координату полигона
        first_coords = next(iter(grouped_coordinates.values()))[0]
        first_coords_x = first_coords[0]
        first_coords_y = first_coords[1]

        # Итерируемся по координатам, формируя 1 половину полигона (нижнюю)
        counter = 0
        for coords in grouped_coordinates.values():
            if counter == 0:
                polygon.append(coords[0])
                counter += 1
                continue

            # Находим элемент с минимальным вторым значением
            min_element = min(coords, key=lambda item: item[1])
            if min_element[0] == first_coords_x + 1 and first_coords_y >= min_element[1]:
                polygon.append(min_element)
                first_coords_x += 1
            elif min_element[0] != first_coords_x + 1:
                polygon.append(central_point)
                first_coords_x += 1
            elif not first_coords_y >= min_element[1]:
                first_coords_x += 1
                continue

        # Итерируемся по координатам, формируя 2 половину полигона (верхнюю)
        counter = 0
        for coords in reversed(grouped_coordinates.values()):
            if counter == 0:
                counter += 1
                continue

            # Находим элемент с максимальным вторым значением
            max_element = max(coords, key=lambda item: item[1])
            if max_element[0] == first_coords_x - 1 and first_coords_y <= max_element[1]:
                polygon.append(max_element)
                first_coords_x -= 1
            elif max_element[0] != first_coords_x - 1:
                polygon.append(central_point)
                first_coords_x -= 1
            elif not first_coords_y <= max_element[1]:
                first_coords_x -= 1
                continue

        return polygon

    def generate_view_polygon(self) -> None:
        """
        Формирует и сохраняет полигон в формате GeoJSON, который содержит информацию
        о станции (координаты, высота, радиус обзора) и сам полигон.
        """

        # Генерация полигона
        geojson_polygon: dict = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "MultiPolygon",
                        "coordinates": [
                            [
                                self.build_polygon()
                            ]
                        ]
                    },
                    "properties": {
                        "station_x": self.obj_x,
                        "station_y": self.obj_y,
                        "station_h": self.obj_height,
                        "radius": self.obj_radius
                    }
                }
            ]
        }

        # Сохранение полигона в файле GeoJSON
        with open(self.geojson_file_path, "w") as file:
            json.dump(geojson_polygon, file, indent=2)

        print("Полигон успешно сгенерирован и сохранен в файле view_polygon.geojson")
