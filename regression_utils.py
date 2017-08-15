import pandas as pd
import data_utils
import datetime
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error
import json


def build_features_two():
	pass

def build_features(network, stop, previous_stop, first_stop = None):
	if 'duration_table' in network[stop].incoming_traffic[previous_stop]:
		duration_tbl = network[stop].incoming_traffic[previous_stop]['duration_table']

		duration_tbl = duration_tbl.sort_values(['start_time'])
		duration_tbl = data_utils.add_day_column(duration_tbl, 'start_time')
		
		x = []
		for idx, row in duration_tbl.iterrows():
			duration_tbl_ten_before = duration_tbl[(duration_tbl['start_time_dt'] > (row["start_time_dt"]  - datetime.timedelta(minutes=10))) & (duration_tbl['start_time_dt'] < (row["start_time_dt"]  ))]
			duration_tbl_twenty_before = duration_tbl[(duration_tbl['start_time_dt'] > (row["start_time_dt"]  - datetime.timedelta(minutes=20))) & (duration_tbl['start_time_dt'] < (row["start_time_dt"]  - datetime.timedelta(minutes=10)))]
			#duration_twent
			res = None
			if len(duration_tbl_ten_before) > 0 and len(duration_tbl_twenty_before) > 0:
				#print(duration_tbl_ten_before)
				#print(duration_tbl_twenty_before)
				res = {'duration_t_minus_1': duration_tbl_ten_before.iloc[0]['duration'].total_seconds(), 'duration_delta': (duration_tbl_ten_before.iloc[0]['duration'] - duration_tbl_twenty_before.iloc[0]['duration']).total_seconds(),
					'label_duration': row['duration'].total_seconds()}
				'''x.append({'duration_t_minus_1': duration_tbl_ten_before.iloc[0]['duration'].total_seconds(), 'duration_delta': (duration_tbl_ten_before.iloc[0]['duration'] - duration_tbl_twenty_before.iloc[0]['duration']).total_seconds(),
					'label_duration': row['duration'].total_seconds()})
				'''
				x.append(res)
				#print row
			else:
				pass

			if first_stop != None:
				first_duration_tbl = network[previous_stop].incoming_traffic[first_stop]
				first_duration_tbl = first_duration_tbl.sort_values(['start_time'])
				first_duration_tbl = data_utils.add_day_column(first_duration_tbl, 'start_time')
		
		return pd.DataFrame(x)
	return None

def first_step_modeling(training, testing):
	clf = linear_model.LinearRegression()
	clf.fit(training[['duration_t_minus_1', 'duration_delta']],training['label_duration'])
	predicted_labels = clf.predict(testing[['duration_t_minus_1', 'duration_delta']])

	error = mean_absolute_error(testing['label_duration'], predicted_labels)

	return error, clf.coef_

def iterate_stops(network_training, network_testing):
	count = 0
	for stop in network_training:
		#actual segment
		for previous_stop in network_training[stop].incoming_traffic:
			if stop in network_testing and previous_stop in network_testing[stop].incoming_traffic:
				res = {}
				training = build_features(network_training, stop, previous_stop)
				testing = build_features(network_testing, stop, previous_stop)
				if training is not None and testing is not None and  len(training) > 0 and len(testing) > 0:
					error, coef = first_step_modeling(training, testing)
					res['{}_{}_error'.format(previous_stop, stop)] = error
					res['{}_{}_coef'.format(previous_stop, stop)] = coef.tolist()
					with open('regression_results/res'+'+'+previous_stop+'+'+stop+'.json', 'w') as f:
						json.dump(res, f)
				#print(training)
				#print(testing)
					if previous_stop in network_training:
						for first_segement_stop in network_training[previous_stop].incoming_traffic:
							if first_segement_stop in network_testing[stop].incoming_traffic:
								pass
								
	print count