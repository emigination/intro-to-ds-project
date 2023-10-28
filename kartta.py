import geopandas
import matplotlib.pyplot as plt
import geoplot as gplt
import pandas as pd

municipality_borders = geopandas.read_file('data/kuntarajat-uusimaa.geojson')
districts_with_sea = geopandas.read_file('data/Helsingin-piirijakorajat-eri-vuosilta-gpkg/v2020.gpkg', layer='peruspiirit-2020').to_crs("EPSG:4326")
helsinki_borders = municipality_borders[municipality_borders["name"] == "Helsinki"]
districts = districts_with_sea.clip(helsinki_borders)

trip_data = pd.read_csv('data/district_trips lopullinen.csv')
total_durations = trip_data.loc[trip_data.Year == 2021].groupby('district')['Total ride duration / population'].sum()

merged_data = pd.merge(districts, total_durations, left_on='NIMI_ISO', right_on='district').explode()

gplt.choropleth(merged_data, hue='Total ride duration / population', cmap='Blues', edgecolor='white', linewidth=1,
                legend=True, legend_kwargs={'location': 'bottom'}, projection=gplt.crs.WebMercator()).get_figure().savefig('map.svg', bbox_inches='tight')
