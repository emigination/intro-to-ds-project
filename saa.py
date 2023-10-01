import numpy as np
from fmiopendata.wfs import download_stored_query
import datetime as dt

year = 2021
startMonth = 4
endMonth = 10
startTime = dt.datetime(year, startMonth, 1).strftime('%Y-%m-%d') + "T00:00:00Z"
endTime = (dt.datetime(year, endMonth+1, 1) - dt.timedelta(days=1)).strftime('%Y-%m-%d')  + "T23:59:59Z"

data = download_stored_query("fmi::observations::weather::daily::multipointcoverage", ["place=Helsinki", "starttime="+startTime, "endtime="+endTime]).data
dateTimes = [dateTime for dateTime in list(data.keys()) if dateTime.strftime('%H') == '00']
dateTimes.sort()
weatherList = []
for dateTime in dateTimes:
  weatherList.append(data[dateTime]['Helsinki Kaisaniemi'])

temperatures = []
precipitations = []
for daysWeather in weatherList:
  temperatures.append(daysWeather['Air temperature']['value'])
  precipitation = daysWeather['Precipitation amount']['value']
  if precipitation == -1:
    precipitation = 0.0
  precipitations.append(precipitation)

outfile = open('temperatures.txt', 'w')
outfile.writelines([str(i)+'\n' for i in temperatures])
outfile.close()

outfile = open('precipitations.txt', 'w')
outfile.writelines([str(i)+'\n' for i in precipitations])
outfile.close()

meanWindSpeeds = []
for month in range(startMonth, endMonth+1):
  startDate = dt.datetime(year, month, 1)
  startTime = startDate.strftime('%Y-%m-%d') + "T00:00:00Z"
  endTime = (dt.datetime(year, month+1, 1) - dt.timedelta(days=1)).strftime('%Y-%m-%d')  + "T23:59:59Z"
  monthlyData = download_stored_query("fmi::observations::weather::hourly::multipointcoverage", ["place=Helsinki", "starttime="+startTime, "endtime="+endTime]).data
  currentDate = startDate
  daysWindSpeeds = []
  for time in sorted(monthlyData.keys()):
    windSpeed = monthlyData[time]['Helsinki Kaisaniemi']['Wind speed']['value']
    if np.isnan(windSpeed):
      continue

    if time.strftime('%Y-%m-%d') == currentDate.strftime('%Y-%m-%d'):
      daysWindSpeeds.append(windSpeed)
    else:
      meanWindSpeeds.append(np.mean(daysWindSpeeds))
      currentDate += dt.timedelta(days=1)
      daysWindSpeeds = [windSpeed]
  meanWindSpeeds.append(np.mean(daysWindSpeeds))

outfile = open('wind_speeds.txt', 'w')
outfile.writelines([str(i)+'\n' for i in meanWindSpeeds])
outfile.close()
