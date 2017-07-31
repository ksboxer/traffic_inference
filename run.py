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
import pickle_finder
import json

def transform(training, arr = None):
	training = data_utils.add_day_column(training)
	training.sort_values(["month","day"])

	training["inferred_trip_id_c"] = training["inferred_trip_id"]

	min_training = training.groupby(["month", "day","vehicle_id","inferred_trip_id"]).apply(lambda x: pd.DataFrame([[x.time_received_dt.max() - x.time_received_dt.min(), x.time_received_dt.min(), x.inferred_trip_id_c.iloc[0]]],columns=['diff','min', "inferred_trip_id"]))
	
	min_training["hour"] = min_training["min"].dt.hour
	min_training = data_processing.hour_break_down(min_training)
	min_training = data_processing.week_day(min_training)

	print min_training

	#print(type(list(min_training["diff"])[0]))

	min_training["diff_sec"] = min_training["diff"].astype('timedelta64[s]')

	if arr == None:
		hist, arr = pd.qcut(min_training["diff_sec"], 3, retbins= True, duplicates="drop")
	if len(arr) < 3:
		hist, arr = pd.cut(min_training["diff_sec"], 3, retbins= True)
	
	arr = list(arr)
	print(arr)
	'''min_training["label"] = ""

	min_training.loc[(min_training["diff_sec"] < arr[1]), ["label"]] = "low"
	min_training.loc[((min_training["diff_sec"] < arr[2]) & (min_training["diff_sec"] >= arr[1])), ["label"]] = "medium"
	min_training.loc[(min_training["diff_sec"] >= arr[2]), ["label"]] = "high"
	'''
	return min_training, list(arr)

	


def main():
	yaml_file_path = sys.argv[1]
	with open(yaml_file_path) as f:
		configs = yaml.load(f)


	if configs["two_segments"]:
		segments = data_loader_preparer.get_agg_twosegments(configs)
		with open('segments{}.pickle'.format(configs['extension']), 'wb') as handle:
			pickle.dump(segments, handle, protocol=pickle.HIGHEST_PROTOCOL)
	else:
		#segments = data_loader_preparer.get_agg(configs)
		#with open('segments.pickle', 'wb') as handle:
		#	pickle.dump(segments, handle, protocol=pickle.HIGHEST_PROTOCOL)
		with open("segments.pickle", "rb") as input_file:
			segments = pickle.load(input_file)

		print(segments)

		for bus_route, next_stop in segments["distance_along_trip"].keys():
			#, next_stop = key
			training, testing =  pickle_finder.check_for_training_testing(configs, bus_route, next_stop)

			#print(training)

			if training is  None:
				training, testing = data_loader_preparer.fake_today_processing(configs,bus_route, next_stop)
				training.to_pickle("training/training#{}#{}#{}.pickle".format(bus_route, next_stop, configs["fake_today"]))
				testing.to_pickle("testing/testing#{}#{}#{}.pickle".format(bus_route, next_stop, configs["fake_today"]))


			training_transformed, arr = transform(training)
			testing_transformed, _ = transform(testing, arr)

			results = modeling.modeling_clf(training_transformed, testing_transformed, bus_route, next_stop)
			with open('results/result#{}#{}#.json'.format(bus_route, next_stop, configs["fake_today"]), 'w') as fp:
				json.dump(results, fp)

			mapping.plot_from_tbl(training, configs, bus_route, next_stop)
		



if __name__ == '__main__':
	print("hello world.. ")
	main()
	