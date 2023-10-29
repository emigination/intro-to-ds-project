import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

data = pd.read_csv('data/district_trips lopullinen.csv')
total_durations = data.loc[data.Year == 2021].groupby('district')['Total ride duration / population'].sum()/3600
station_densities = data.groupby('district')['Stations/km2'].first()
capacities = data.groupby('district')['Capacity'].first()

sb.regplot(x=station_densities, y=total_durations)
plt.xlabel('Stations per square kilometre')
plt.ylabel('Total ride duration per population, hours')
plt.savefig('stations_vs_duration.png')
plt.clf()

sb.regplot(x=capacities, y=total_durations)
plt.xlabel('Capacity per population')
plt.ylabel('Total ride duration per population, hours')
plt.savefig('capacity_vs_duration.png')
plt.clf()


data['total_duration'] = data['Mean_duration'] * data['count']
durations_by_year = (data.groupby('Year')['total_duration'].sum()/3600/1000)
station_count_by_year = data.groupby(['district', 'Year'])['station_count'].first().groupby('Year').sum()
fig, ax1 = plt.subplots()
ax1.set_ylabel('Number of stations')
ax1.bar(station_count_by_year.index, station_count_by_year, color='lightblue')
ax2 = ax1.twinx()
ax2.set_xlabel('Year')
ax2.set_ylabel('Total ride duration, thousands of hours')
ax2.plot(durations_by_year.index, durations_by_year, color='blue')
plt.savefig('stations_and_duration_by_year.png')
plt.clf()

durations_by_district_and_year = data.groupby(['district', 'Year'])['Total ride duration / population'].sum()/3600
districts_with_multiple_years = durations_by_district_and_year.groupby('district').count() > 1
filtered_durations = durations_by_district_and_year.loc[districts_with_multiple_years[districts_with_multiple_years].index]
sb.lineplot(x=filtered_durations.index.get_level_values('Year'), y=filtered_durations,
            hue=filtered_durations.index.get_level_values('district'), style=filtered_durations.index.get_level_values('district'))
plt.xlabel('Year')
plt.ylabel('Total ride duration per population, hours')
handles, labels = plt.gca().get_legend_handles_labels()
filtered_total_durations = total_durations.loc[districts_with_multiple_years[districts_with_multiple_years].index]
df = pd.DataFrame({'district': filtered_total_durations.index, 'total_durations': filtered_total_durations.values}).sort_values(by='total_durations', ascending=False)
order = df.index
plt.legend([handles[i] for i in order],[labels[i].title() for i in order], loc='right')
plt.savefig('duration_by_year_and_district.svg', bbox_inches='tight')

