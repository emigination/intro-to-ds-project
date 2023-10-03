import numpy as np
import pandas as pd
import seaborn as so
import statsmodels.api as sm

trips = pd.read_csv('daily_trips.csv')

temperatures = np.loadtxt('temperatures.txt')
precipitations = np.loadtxt('precipitations.txt')
precipitationsBoolean = [bool(precipitation) for precipitation in precipitations]
windSpeeds = np.loadtxt('wind_speeds.txt')

so.scatterplot(x=temperatures, y=trips['Trips']).figure.savefig('trips_vs_temperature.png')
so.scatterplot(x=precipitations, y=trips['Trips']).figure.savefig('trips_vs_precipitation.png')
so.scatterplot(x=windSpeeds, y=trips['Trips']).figure.savefig('trips_vs_wind_speed.png')
so.barplot(x=precipitationsBoolean, y=trips['Trips']).figure.savefig('trips_vs_rain.png')

print('Correlation coefficient between trips and temperature:', np.corrcoef(temperatures, trips['Trips'])[0,1])
print('Correlation coefficient between trips and precipitation:', np.corrcoef(precipitations, trips['Trips'])[0,1])
print('Correlation coefficient between trips and wind speed:', np.corrcoef(windSpeeds, trips['Trips'])[0,1])
print('Correlation coefficient between trips and rain:', np.corrcoef(precipitationsBoolean, trips['Trips'])[0,1])

weather = pd.DataFrame({'Temperature': temperatures, 'Precipitation': precipitations, 'Wind speed': windSpeeds})
temperatureAndWind = pd.DataFrame({'Temperature': temperatures, 'Wind speed': windSpeeds})

X =temperatureAndWind
y=trips.Trips
X2 = sm.add_constant(X)
est = sm.OLS(y, X2)
est2 = est.fit()
est2.summary()
