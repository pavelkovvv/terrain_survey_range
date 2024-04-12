import geopandas as gpd
import matplotlib.pyplot as plt

# Чтение файла GeoJSON
geojson_file = "example_true_polygon.geojson"
gdf = gpd.read_file(geojson_file)

# Создание графика с указанием размеров
fig, ax = plt.subplots(figsize=(5, 5))

# Установка пределов по осям X и Y
ax.set_xlim(0, 50)
ax.set_ylim(0, 50)

# Визуализация геометрии
gdf.plot(ax=ax)

# Отображение графика
plt.show()
