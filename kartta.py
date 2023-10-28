import geopandas
import matplotlib.pyplot as plt
import pandas as pd

municipality_borders = geopandas.read_file('data/kuntarajat-uusimaa.geojson')
districts_with_sea = geopandas.read_file('data/Helsingin-piirijakorajat-eri-vuosilta-gpkg/v2020.gpkg', layer='peruspiirit-2020').to_crs("EPSG:4326")
helsinki_borders = municipality_borders[municipality_borders["name"] == "Helsinki"]
districts = districts_with_sea.clip(helsinki_borders)

districts.plot()

plt.show()

trip_data = pd.read_csv('data/district_trips lopullinen.csv')
total_durations = trip_data.groupby('district')['Total ride duration / population'].sum()

df = pd.merge(total_durations, districts, left_on='district', right_on='NIMI_ISO')
