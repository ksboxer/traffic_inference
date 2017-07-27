import yaml
import sys
import data_loader_utils
import data_utils
import mapping
import data_loader_preparer
import pickle
import pandas as pd
import data_processing
import modeling
import numpy as np
import data_utils

def transform(training, arr):
	min_training = training.groupby(["month", "day","vehicle_id","inferred_trip_id"]).apply(lambda x: pd.DataFrame([[x.time_received_dt.max() - x.time_received_dt.min(), x.time_received_dt.min()]],columns=['diff','min']))
	
	print(type(list(min_training["diff"])[0]))

	min_training["diff_sec"] = min_training["diff"].astype('timedelta64[s]')

	if arr == None:
		hist, arr = pd.qcut(min_training["diff_sec"], 3, retbins= True, duplicates="drop")
	
	return training, arr

	


def main():
	yaml_file_path = sys.argv[1]
	with open(yaml_file_path) as f:
		configs = yaml.load(f)


	#segments = data_loader_preparer.get_agg(configs)


	#with open('segments.pickle', 'wb') as handle:
	#	pickle.dump(segments, handle, protocol=pickle.HIGHEST_PROTOCOL)
	with open("segments.pickle", "rb") as input_file:
		segments = pickle.load(input_file)

	print(segments)

	for bus_route, next_stop in segments["distance_along_trip"].keys():
		#, next_stop = key
		training, testing = data_loader_preparer.fake_today_processing(configs,bus_route, next_stop)
		training.to_pickle("training#{}#{}#{}.pickle".format(bus_route, next_stop, configs["fake_today"]))
		testing.to_pickle("testing#{}#{}#{}.pickle".format(bus_route, next_stop, configs["fake_today"]))

		training = data_utils.add_day_column(training)
		testing = data_utils.add_day_column(testing)

		training.sort_values(["month","day"])
		testing.sort_values(["month","day"])

		f = {'A':['min'], 'B':['max']}

		min_training = training.groupby(["month", "day","vehicle_id","inferred_trip_id"]).apply(lambda x: pd.DataFrame([[x.time_received_dt.max() - x.time_received_dt.min(), x.time_received_dt.min()]],columns=['diff','min']))
		min_testing = testing.groupby(["month", "day","vehicle_id","inferred_trip_id"]).apply(lambda x: pd.DataFrame([[x.time_received_dt.max() - x.time_received_dt.min(), x.time_received_dt.min()]],columns=['diff','min']))
	
		min_training["diff_sec"] = min_training["diff"].astype('timedelta64[s]')
		min_testing["diff_sec"] = min_testing["diff"].astype('timedelta64[s]')
	hist, arr = pd.qcut(min_training["diff_sec"], 3, retbins= True, duplicates="drop")
	print(arr)
	#print(min_training)
	#print(pd.to_datetime(max_training[2]) - pd.to_datetime(min_training[2]))
	
	#print(training.groupby(["month", "day"])["time_received"].min())

	#training_table, arr = data_processing.table_processing_training(training)
	#testing_table = data_processing.table_processing_testing(testing, arr)

	#mapping.plot_from_tbl(training)


	
	#print training
	#print(training_table['speed_label'].value_counts())
	#print(training)
	#print(training[training['speed'] == 0])
	#print testing_table
	#modeling.modeling_svm(training_table, testing_table)
	#print(training_table["speed_label"].value_counts())
	#print(training_table)
	#print(testing_table)
	'''tbl = data_loader_utils.read_in_file_by_date(configs)
	vehicle_id_tbl = data_utils.rows_by_vehicle_id(tbl, configs)
	tbl_shift = data_utils.transform(vehicle_id_tbl)
	print tbl_shift
	mapping.plot_from_tbl(vehicle_id_tbl)'''


if __name__ == '__main__':
	print("hello world.. traffic is solvable problem")
	main()
	