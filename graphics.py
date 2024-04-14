import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import geopandas as gpd


class Graphics:
    """
    Используется для создания графиков на основе данных о высотах местности и геометрии,
    представленной в формате GeoJson.
    """

    LINE_THICKNESS: float = 0.5
    CHART_DIVISION_PERIOD: int = 2
    BOLD_POINT: int = 100
    CHART_SIZE: int = 8

    def __init__(
            self,
            height_csv_file: str,
            matrix_len_x: int,
            matrix_len_y: int,
            geojson_file_path: str,
            middle_x: int,
            middle_y: int,
    ):
        self.height_csv_file = height_csv_file
        self.matrix_len_x = matrix_len_x
        self.matrix_len_y = matrix_len_y
        self.geojson_file_path = geojson_file_path
        self.middle_x = middle_x
        self.middle_y = middle_y

    def converting_to_matrix(self) -> np.ndarray:
        """Позволяет преобразовать csv-файл в матрицу определённой размерности."""

        heights_data = np.genfromtxt(self.height_csv_file, delimiter=',')
        heights_matrix = heights_data.reshape((self.matrix_len_x, self.matrix_len_y))

        return heights_matrix

    def make_matrix_height_plot(self) -> None:
        """Позволяет создать график с матрицей высот."""

        plt.contourf(self.converting_to_matrix(), cmap='terrain')

        # Добавление цветовой шкалы
        plt.colorbar(label='Высота')

        # Добавление заголовка и меток осей
        plt.title('Визуализация матрицы высот')
        plt.xlabel('Ширина')
        plt.ylabel('Высота')

        # Отображение графика
        plt.figure(1)

    def make_result_polygon_plot(self) -> None:
        """Позволяет создать итоговый график с полигоном."""

        # Чтение файла GeoJSON
        geojson_file = self.geojson_file_path
        gdf = gpd.read_file(geojson_file)

        # Создание графика с указанием размеров
        fig, ax = plt.subplots(figsize=(self.CHART_SIZE, self.CHART_SIZE))

        # Добавление синей точки с координатами object_x и object_y
        ax.scatter(self.middle_x, self.middle_y, color='blue', label='Центр полигона (местонахождение станции)', s=self.BOLD_POINT)

        # Визуализация геометрии сеткой и мелкими единицами
        gdf.plot(ax=ax, alpha=self.LINE_THICKNESS, edgecolor='black', linewidth=self.LINE_THICKNESS, cmap='viridis', label='Итоговый полигон')

        # Добавление сетки и делений с мелкими единицами
        ax.set_xticks(range(0, self.matrix_len_x + 1, self.CHART_DIVISION_PERIOD))
        ax.set_yticks(range(0, self.matrix_len_y + 1, self.CHART_DIVISION_PERIOD))
        ax.grid(which='both', linestyle='--', linewidth=self.LINE_THICKNESS, color='gray', alpha=self.LINE_THICKNESS)

        # Добавление легенды
        polygon_patch = mpatches.Patch(color='purple', label='Итоговый полигон')
        polygon_middle = mpatches.Patch(color='blue', label='Центр полигона (местонахождение станции)')
        ax.legend(handles=[polygon_patch, polygon_middle])

        # Установка пределов по осям X и Y
        ax.set_xlim(0, self.matrix_len_x)
        ax.set_ylim(0, self.matrix_len_y)

        # Добавление заголовка и меток осей
        ax.set_title('Полигон, описывающий зону доступной к обзору местности')
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')

        # Отображение графика
        plt.tight_layout()
        plt.figure(2)
