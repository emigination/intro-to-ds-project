import numpy as np
from fmiopendata.wfs import download_stored_query
import datetime as dt
data = download_stored_query("fmi::observations::weather::daily::multipointcoverage", ["place=Helsinki", "starttime=2021-01-01", "endtime=2021-12-31"]).data
dates = sorted(list(data.keys()))
weatherByDay = {}
weatherList = []
for date in dates:
  weatherByDay[date] = data[date]['Helsinki Kaisaniemi']
  weatherList.append(data[date]['Helsinki Kaisaniemi'])

temperatures = []
precipitations = []
for i, daysWeather in enumerate(weatherList):
  temperature = daysWeather['Air temperature']['value']
  if np.isnan(temperature):
    previous = weatherList[i-1]['Air temperature']['value']
    following = weatherList[i+1]['Air temperature']['value']
    if np.isnan(previous):
      temperatures.append(following)
    elif np.isnan(following):
      temperatures.append(previous)
    else:
      temperature = (weatherList[i-1]['Air temperature']['value'] + weatherList[i+1]['Air temperature']['value'])/2
  else:
    temperatures.append(temperature)
  precipitation = daysWeather['Precipitation amount']['value']
  if precipitation == -1:
    precipitation = 0
  precipitations.append(precipitation)

imputedPrecipitations = precipitations.copy()
for i, precipitation in enumerate(precipitations):
  if np.isnan(precipitation):
    previous = precipitations[i-1]
    following = precipitations[i+1]
    if np.isnan(previous):
      imputedPrecipitations[i] = following
    elif np.isnan(following):
      imputedPrecipitations[i] = previous
    else:
      imputedPrecipitations[i] = (previous + following)/2

print(imputedPrecipitations)
