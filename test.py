import geopandas as gpd
import matplotlib.pyplot as plt

# Чтение файла GeoJSON
geojson_file = "view_polygon.geojson"
gdf = gpd.read_file(geojson_file)

# Создание графика
fig, ax = plt.subplots()

# Визуализация геометрий
gdf.plot(ax=ax)

# Отображение графика
plt.show()
