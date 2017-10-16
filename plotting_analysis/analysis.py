import os, sys
import pickle
import mapping
import pandas as pd


from glob import glob
import json


lib_path = os.path.abspath('./utils')
sys.path.insert(0,lib_path)

import json

import combination

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

with open('training_full.pickle', 'rb') as f:
	network_training = pickle.load(f)

with open('testing_full.pickle', 'rb') as f:
	network_testing = pickle.load(f)

full_network = combination.combine_two_networks(network_training, network_testing)

print('Number of Bus stops: {}'.format(len(full_network)))

count = 0
for stop in full_network:
	count = count + len(full_network[stop].incoming_traffic)

print('Number of Segments: {}'.format(count))


#print(full_network[full_network.keys()[0]].incoming_traffic['raw_data'])

full_lat_lon = pd.DataFrame()
for filename in glob('regression_results_3/*.html'):
        if 'classFalse'  in filename:
                with open(filename, 'r') as f:
                        results = json.load(f)
                results_sub = results[results.keys()[0]]
                previous_stop = results_sub['previous_stop']
                stop = results_sub['stop']
		raw_data = full_network[stop].incoming_traffic[previous_stop]['raw_data']
		#full_lat_lon = full_lat_lon.append(raw_data)
		if 'duration_table' in full_network[stop].incoming_traffic[previous_stop]:
			duration_table = full_network[stop].incoming_traffic[previous_stop]['duration_table']
			#print(list(duration_table))
			#duration_table.sort_values([])
			#duration_table = duration_table.sort_values(['start_time'])
			#fig = plt.figure(figsize = (50,20))
			#plt.plot(duration_table['start_time'],duration_table['duration'])
			print('{} {}'.format(previous_stop, stop))
			#fig.savefig('segment_plot/{}_{}.png'.format(previous_stop, stop))
			duration_table['start_time'] = pd.to_datetime(duration_table['start_time'])
			duration_table['month'] = duration_table['start_time'].dt.month
			duration_table['day'] = duration_table['start_time'].dt.day
			duration_table['hour'] = duration_table['start_time'].dt.hour
			time_frame_hours = duration_table.groupby(['month', 'day', 'hour'])
			final_res = {}
			for (month,day,hour), group in time_frame_hours:
				group['duration_seconds'] = group['duration'].astype('timedelta64[s]')
				std_hour = group['duration_seconds'].std()
				final_res['{}_{}_{}'.format(month, day, hour)] = {}
				final_res['{}_{}_{}'.format(month,day,hour)]['std'] =  std_hour
				final_res['{}_{}_{}'.format(month,day,hour)]['count'] = len(group)
				print(group['duration_seconds'])
				print('mean: {}'.format(group['duration_seconds'].mean()))
				final_res['{}_{}_{}'.format(month,day,hour)]['mean'] = group['duration_seconds'].mean()
			with open('variation_segments_count/{}_{}.json'.format(previous_stop, stop), 'w') as fp:
				json.dump(final_res, fp)	
print(len(full_lat_lon))

#full_lat_lon = full_lat_long.sample(frac= .5)
#mapping.plot_from_tbl_quick(full_lat_lon, 'test')
