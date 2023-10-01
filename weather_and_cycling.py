import numpy as np
import pandas as pd
import seaborn as so

temperatures = np.loadtxt('temperatures.txt')
precipitations = np.loadtxt('precipitations.txt')
windSpeeds = np.loadtxt('wind_speeds.txt')

trips = pd.read_csv('daily_trips.csv')

# so.scatterplot(x=temperatures, y=trips['Trips']).figure.savefig('trips_vs_temperature.png')
# so.scatterplot(x=precipitations, y=trips['Trips']).figure.savefig('trips_vs_precipitation.png')
# so.scatterplot(x=windSpeeds, y=trips['Trips']).figure.savefig('trips_vs_wind_speed.png')

precipitationsBoolean = [True if precipitation > 0 else False for precipitation in precipitations]
so.scatterplot(x=temperatures, y=trips['Trips'], hue=precipitationsBoolean).figure.savefig('trips_vs_temperature_and_precipitation.png')

print('Correlation coefficient between trips and temperature:', np.corrcoef(temperatures, trips['Trips'])[0,1])
print('Correlation coefficient between trips and precipitation:', np.corrcoef(precipitations, trips['Trips'])[0,1])
print('Correlation coefficient between trips and wind speed:', np.corrcoef(windSpeeds, trips['Trips'])[0,1])
print('Correlation coefficient between trips and rain:', np.corrcoef(precipitationsBoolean, trips['Trips'])[0,1])
