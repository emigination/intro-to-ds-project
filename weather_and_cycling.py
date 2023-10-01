import numpy as np
import pandas as pd
import seaborn as sb

# temperatures = np.loadtxt('temperatures.txt')
# precipitations = np.loadtxt('precipitations.txt')
# windSpeeds = np.loadtxt('wind_speeds.txt')

year = 2021
months = range(4, 11)
monthlyTrips = []
for month in months:
  if month < 10:
    monthString = '0'+ str(month)
  else:
    monthString = str(month)
  infile = open('data/od-trips-'+ str(year) + '/2021-'+monthString+'.csv', 'r')
  df = pd.read_csv(infile, sep=',')
  infile.close()
  monthlyTrips.append(df)
allTrips = pd.concat(monthlyTrips)
allTrips.sort_values(by=['Departure'], inplace=True, ignore_index=True)
allTrips['Date'] = pd.to_datetime(allTrips['Departure'], format='ISO8601').dt.date
