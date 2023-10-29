import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

data = pd.read_csv('data/district_trips lopullinen.csv')
total_durations = data.loc[data.Year == 2021].groupby('district')['Total ride duration / population'].sum()/3600
# df = df.sort_values(by='Total ride duration / population', ascending=False)
station_densities = data.groupby('district')['Stations/km2'].first()
capacities = data.groupby('district')['Capacity'].first()

# sb.regplot(x=station_densities, y=total_durations)
# plt.xlabel('Stations per square kilometre')
# plt.ylabel('Total ride duration per population, hours')
# plt.savefig('stations_vs_duration.png')
# plt.clf()

# sb.regplot(x=capacities, y=total_durations)
# plt.xlabel('Capacity per population')
# plt.ylabel('Total ride duration per population, hours')
# plt.savefig('capacity_vs_duration.png').

# create dataframe with columns district and total_durations, sorted by total_durations, descendings
df = pd.DataFrame({'district': total_durations.index, 'total_durations': total_durations.values}).sort_values(by='total_durations', ascending=False)
durations_by_district_and_year = data.groupby(['district', 'Year'])['Total ride duration / population'].sum()/3600
sb.lineplot(x=durations_by_district_and_year.index.get_level_values('Year'), y=durations_by_district_and_year,
            hue=durations_by_district_and_year.index.get_level_values('district'), style=durations_by_district_and_year.index.get_level_values('district'))
plt.xlabel('Year')
plt.ylabel('Total ride duration per population, hours')
#sort legend in the order df.district is sorted
handles, labels = plt.gca().get_legend_handles_labels()
order = df.index.get_indexer_for(labels)
plt.legend([handles[order.get_loc(label)] for label in labels], labels, loc='upper left')

# plt.savefig('duration_by_year.png')
plt.show()
