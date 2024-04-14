import argparse
import yaml
import matplotlib.pyplot as plt

from graphics import Graphics
from poligon_build import PolygonBuild


def main():
    # Создаем парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Filter target coordinates based on radar position and height.")

    # Добавляем аргументы
    parser.add_argument("-x", type=int, help="X coordinate of the radar")
    parser.add_argument("-y", type=int, help="Y coordinate of the radar")
    parser.add_argument("-H", type=int, help="Height of the radar")
    parser.add_argument("-r", type=int, help="Radar's radius of detection")

    # Считываем аргументы командной строки
    args = parser.parse_args()

    # Проверяем, что все обязательные аргументы предоставлены
    if None in (args.x, args.y, args.H, args.r):
        parser.error("Пожалуйста, введите все необходимые параметры.")

    # Открываем yaml-файл
    with open('config.yaml', 'r') as file:
        # Загружаем данные из YAML файла
        config_data = yaml.safe_load(file)

    matrix_height_file_path: str = str(config_data['data']['matrix_file_path'])
    matrix_len_x: int = int(config_data['data']['matrix_len_x'])
    matrix_len_y: int = int(config_data['data']['matrix_len_y'])
    geojson_file_path: str = str(config_data['data']['geojson_file_path'])

    try:
        # Создание объекта графики с определёнными параметрами
        graph = Graphics(
            matrix_height_file_path,
            matrix_len_x,
            matrix_len_y,
            geojson_file_path,
            args.x,
            args.y,
        )

        # Построим график матрицы высот
        graph.make_matrix_height_plot()

        # Создадим объект с настройками для построения полигона
        polygon = PolygonBuild(
            matrix_height_file_path,
            matrix_len_x,
            matrix_len_y,
            args.x,
            args.y,
            args.r,
            args.H,
            geojson_file_path,
        )

        # Создадим .geojson-файл с полигоном
        polygon.generate_view_polygon()

        # Выведем график получившегося полигона
        graph.make_result_polygon_plot()

        # Отображение всех графиков
        plt.show()

    except Exception:
        print('Невозможно построить график, так как не было найдено ни одной точки.')


if __name__ == '__main__':
    main()
