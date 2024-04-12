import geopandas as gpd
import matplotlib.pyplot as plt

# Чтение файла GeoJSON
geojson_file = "view_polygon.geojson"
gdf = gpd.read_file(geojson_file)

# Создание графика
fig, ax = plt.subplots()

# Визуализация геометрий
gdf.plot(ax=ax, facecolor='yellow', edgecolor='blue')  # устанавливаем цвет границы и прозрачный цвет заполнения

# Отображение графика
plt.show()
