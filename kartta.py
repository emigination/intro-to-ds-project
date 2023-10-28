import geopandas
import matplotlib.pyplot as plt

municipality_borders = geopandas.read_file('data/kuntarajat-uusimaa.geojson')
# districts =geopandas.read_file('data/Helsingin-piirijakorajat-eri-vuosilta-gpkg/v2020.gpkg', layer='Helsingin piirijakorajat 2020')
districts = geopandas.read_file('data/Helsingin-piirijakorajat-eri-vuosilta-gpkg/v2020.gpkg').to_crs("EPSG:4326")

helsinki = municipality_borders[municipality_borders["name"] == "Helsinki"]

geopandas.overlay(districts, helsinki, how='intersection').plot()

plt.show()
