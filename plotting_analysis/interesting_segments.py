import pickle
import pandas as pd

with open('training_full.pickle') as f:
	data = pickle.load(f)

print(data.keys())

listings = []

for stop in data:
	for previous_stop in data[stop].incoming_traffic:
		print('{}, {}'.format(previous_stop, stop))
		if 'raw_data' in data[stop].incoming_traffic[previous_stop]:
			print('raw data : {}'.format(len(data[stop].incoming_traffic[previous_stop]['raw_data'])))
		if 'duration_table' in  data[stop].incoming_traffic[previous_stop]:
			print('duration_table : {}'.format(len(data[stop].incoming_traffic[previous_stop]['duration_table'])))
			listings.append({'previous_stop':previous_stop, 'stop': stop, 'len': len(data[stop].incoming_traffic[previous_stop]['duration_table'])})

df = pd.DataFrame(listings)
df = df.sort_values(['len'], ascending = False)
print(df)