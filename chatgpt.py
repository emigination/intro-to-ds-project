import numpy as np
import pandas as pd
from fmiopendata.wfs import download_stored_query
import datetime as dt

def date_range(start_date, end_date, max_days):
  current_date = start_date
  while (end_date - current_date).days > max_days:
    chunk_end = current_date + dt.timedelta(days=max_days-1)
    yield (current_date, chunk_end)
    current_date = chunk_end + dt.timedelta(days=1)
  yield (current_date, end_date)


def fetch_weather_data(start_date, end_date):
  weather_list = []
  weather_by_day = {}
  date_times = []
  for start, end in date_range(start_date, end_date, 372):
    start_string = start.strftime('%Y-%m-%d') + "T00:00:00Z"
    end_string = end.strftime('%Y-%m-%d') + "T23:59:59Z"
    data_chunk = download_stored_query("fmi::observations::weather::daily::multipointcoverage", ["place=Helsinki", "starttime="+start_string, "endtime="+ end_string]).data
    date_times_chunk = [date_time for date_time in list(data_chunk.keys()) if date_time.strftime('%H') == '00']
    weather_list += [data_chunk[date_time]['Helsinki Kaisaniemi'] for date_time in date_times_chunk]
    weather_by_day.update({date_time: data_chunk[date_time]['Helsinki Kaisaniemi'] for date_time in date_times_chunk})
    date_times += date_times_chunk

  temperatures = [days_weather['Air temperature']['value'] for days_weather in weather_list]

  precipitations = []
  for days_weather in weather_list:
    precipitation = days_weather['Precipitation amount']['value']
    if precipitation == -1:
      precipitation = 0.0
    precipitations.append(precipitation)

  mean_wind_speeds = []
  wind_speeds_by_day = {}
  means_by_day = {}
  for start, end in date_range(start_date, end_date, 31):
    start_string = start.strftime('%Y-%m-%d') + "T00:00:00Z"
    end_string = end.strftime('%Y-%m-%d') + "T23:59:59Z"
    data_chunk = download_stored_query("fmi::observations::weather::hourly::multipointcoverage", ["place=Helsinki", "starttime="+start_string, "endtime="+ end_string]).data
    current_date = start
    days_wind_speeds = []
    for time in sorted(data_chunk.keys()):
      wind_speed = data_chunk[time]['Helsinki Kaisaniemi']['Wind speed']['value']
      if time.date() != current_date:
        mean_wind_speeds.append(np.mean(days_wind_speeds))
        wind_speeds_by_day[current_date] = days_wind_speeds
        means_by_day[current_date] = np.mean(days_wind_speeds)
        current_date += dt.timedelta(days=1)
        days_wind_speeds = []
      if not np.isnan(wind_speed):
        days_wind_speeds.append(wind_speed)
  mean_wind_speeds.append(np.mean(days_wind_speeds))
  wind_speeds_by_day[current_date] = days_wind_speeds
  means_by_day[current_date] = np.mean(days_wind_speeds)

  print(len(date_times), len(temperatures), len(precipitations), len(mean_wind_speeds), len(wind_speeds_by_day), len(means_by_day))
  print(sorted(list(set(weather_by_day.keys()) - set(means_by_day.keys()))))
  weather_df = pd.DataFrame({'Date': date_times, 'Temperature': temperatures, 'Precipitation': precipitations, 'Wind Speed': mean_wind_speeds})
  weather_df.to_csv('weather_table.csv', index=False)

fetch_weather_data(dt.date(2020, 4, 1), dt.date(2021, 10, 31))
