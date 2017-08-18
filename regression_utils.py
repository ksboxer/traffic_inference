import pandas as pd
import data_utils
import datetime
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error
import json


def all_previous_segments_build_features(network, stop, previous_stop):
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
				#x.append(res)
				#print row

				temp_res = []
				for first_stop in network[previous_stop].incoming_traffic:
					if 'duration_table' in network[previous_stop].incoming_traffic[first_stop]:
						first_duration_tbl = network[previous_stop].incoming_traffic[first_stop]['duration_table']
						first_duration_tbl = first_duration_tbl.sort_values(['start_time'])
						first_duration_tbl = data_utils.add_day_column(first_duration_tbl, 'start_time')
						
						first_duration_tbl_ten_before = first_duration_tbl[(first_duration_tbl['start_time_dt'] > (row["start_time_dt"]  - datetime.timedelta(minutes=10))) & (first_duration_tbl['start_time_dt'] < (row["start_time_dt"]  ))]
						first_duration_tbl_twenty_before = first_duration_tbl[(first_duration_tbl['start_time_dt'] > (row["start_time_dt"]  - datetime.timedelta(minutes=20))) & (first_duration_tbl['start_time_dt'] < (row["start_time_dt"]  - datetime.timedelta(minutes=10)))]
					
						if len(first_duration_tbl_ten_before) > 0 and len(first_duration_tbl_twenty_before) > 0:
							res_secondary = {}
							res_secondary['f_duration_t_minus_1'] = first_duration_tbl_ten_before.iloc[0]['duration'].total_seconds()
							res_secondary['f_duration_delta'] = (first_duration_tbl_ten_before.iloc[0]['duration'] - first_duration_tbl_twenty_before.iloc[0]['duration']).total_seconds()
							temp_res.append(res_secondary)
				temp_res = pd.DataFrame(temp_res)
				if len(temp_res) > 1:
					res['f_duration_t_minus_1'] = temp_res['f_duration_t_minus_1'].mean()
					res['f_duration_t_minus_1_std'] = temp_res['f_duration_t_minus_1'].std()
					res['f_duration_delta'] = temp_res['f_duration_delta'].mean()
					res['f_duration_delta_std'] = temp_res['f_duration_delta'].std()
					x.append(res)
		if len(x) > 0:
			return pd.DataFrame(x)
	return None

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
				#x.append(res)
				#print row

				if first_stop != None:
					if 'duration_table' in network[previous_stop].incoming_traffic[first_stop]:
						first_duration_tbl = network[previous_stop].incoming_traffic[first_stop]['duration_table']
						first_duration_tbl = first_duration_tbl.sort_values(['start_time'])
						first_duration_tbl = data_utils.add_day_column(first_duration_tbl, 'start_time')
						
						first_duration_tbl_ten_before = first_duration_tbl[(first_duration_tbl['start_time_dt'] > (row["start_time_dt"]  - datetime.timedelta(minutes=10))) & (first_duration_tbl['start_time_dt'] < (row["start_time_dt"]  ))]
						first_duration_tbl_twenty_before = first_duration_tbl[(first_duration_tbl['start_time_dt'] > (row["start_time_dt"]  - datetime.timedelta(minutes=20))) & (first_duration_tbl['start_time_dt'] < (row["start_time_dt"]  - datetime.timedelta(minutes=10)))]
					
						if len(first_duration_tbl_ten_before) > 0 and len(first_duration_tbl_twenty_before) > 0:
							res['f_duration_t_minus_1'] = first_duration_tbl_ten_before.iloc[0]['duration'].total_seconds()
							res['f_duration_delta'] = (first_duration_tbl_ten_before.iloc[0]['duration'] - first_duration_tbl_twenty_before.iloc[0]['duration']).total_seconds()
							x.append(res)
				else:
					x.append(res)
		return pd.DataFrame(x)
	return None

def previous_segment_modeling(training,testing):
	clf = linear_model.LinearRegression()
	#print(training)
	clf.fit(training[['duration_t_minus_1', 'duration_delta',  'f_duration_t_minus_1', 'f_duration_delta']],training['label_duration'])
	predicted_labels = clf.predict(testing[['duration_t_minus_1', 'duration_delta', 'f_duration_t_minus_1', 'f_duration_delta']])

	error = mean_absolute_error(testing['label_duration'], predicted_labels)
	mean_labels = testing['label_duration'].mean()
	std_labels = testing['label_duration'].std()

	return error, clf.coef_, mean_labels, std_labels

def first_step_modeling(training, testing):
	clf = linear_model.LinearRegression()
	clf.fit(training[['duration_t_minus_1', 'duration_delta']],training['label_duration'])
	predicted_labels = clf.predict(testing[['duration_t_minus_1', 'duration_delta']])

	error = mean_absolute_error(testing['label_duration'], predicted_labels)
	mean_labels = testing['label_duration'].mean()
	std_labels = testing['label_duration'].std()

	return error, clf.coef_, mean_labels, std_labels

def all_segments_modeling(training,testing):
	#print(testing)
	clf = linear_model.LinearRegression()
	clf.fit(training[['duration_t_minus_1', 'duration_delta',  'f_duration_t_minus_1', 'f_duration_delta', 'f_duration_t_minus_1_std','f_duration_delta_std']],training['label_duration'])
	predicted_labels = clf.predict(testing[['duration_t_minus_1', 'duration_delta', 'f_duration_t_minus_1', 'f_duration_delta','f_duration_t_minus_1_std','f_duration_delta_std']])

	error = mean_absolute_error(testing['label_duration'], predicted_labels)
	mean_labels = testing['label_duration'].mean()
	std_labels = testing['label_duration'].std()

	return error, clf.coef_, mean_labels, std_labels

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
					error, coef, mean, std = first_step_modeling(training, testing)
					res['one_segment'] = {}
					res['one_segment']['error'.format(previous_stop, stop)] = error
					res['one_segment']['coef'.format(previous_stop, stop)] = coef.tolist()
					res['one_segment']['label_mean'] = mean
					res['one_segment']['label_std'] = std
					#with open('regression_results/res'+'+'+previous_stop+'+'+stop+'.json', 'w') as f:
					#	json.dump(res, f)
				#print(training)
				#print(testing)
					res['previous_segments'] ={}
					if previous_stop in network_training:
						for first_segement_stop in network_training[previous_stop].incoming_traffic:
							if first_segement_stop in network_testing[previous_stop].incoming_traffic:
								training = build_features(network_training, stop, previous_stop, first_segement_stop)
								testing = build_features(network_testing, stop, previous_stop, first_segement_stop)
								if training is not None and testing is not None and len(training)> 0 and len(testing) > 0:
									error , coef, _, _ = previous_segment_modeling(training, testing)
									key_next = '{}_{}_{}'.format(first_segement_stop,previous_stop, stop)
									res['previous_segments'][key_next] = {}
									res['previous_segments'][key_next]['error'] = error
									res['previous_segments'][key_next]['coef'] = coef.tolist()

						training = all_previous_segments_build_features(network_training, stop, previous_stop)
						testing = all_previous_segments_build_features(network_testing, stop, previous_stop)
						if training is not None and testing is not None and len(training)> 0 and len(testing) > 0:
							error, coef, _, _ = all_segments_modeling(training, testing)
							res['combined_all_previous_segments'] = {}
							res['combined_all_previous_segments']['error'] = error
							res['combined_all_previous_segments']['coef'] = coef.tolist()
						with open('regression_results/res'+'+'+previous_stop+'+'+stop+'.json', 'w') as f:
							print('regression_results/res'+'+'+previous_stop+'+'+stop+'.json')
							json.dump(res, f)
	print count