import geopandas
import matplotlib.pyplot as plt

municipality_borders = geopandas.read_file('data/kuntarajat-uusimaa.geojson')
districts_with_sea = geopandas.read_file('data/Helsingin-piirijakorajat-eri-vuosilta-gpkg/v2020.gpkg', layer='peruspiirit-2020').to_crs("EPSG:4326")
helsinki_borders = municipality_borders[municipality_borders["name"] == "Helsinki"]
districts = districts_with_sea.clip(helsinki_borders)

districts.plot()

plt.show()
