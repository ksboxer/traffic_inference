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

def transform(training, arr = None):
	training = data_utils.add_day_column(training)
	training.sort_values(["month","day"])

	min_training = training.groupby(["month", "day","vehicle_id","inferred_trip_id"]).apply(lambda x: pd.DataFrame([[x.time_received_dt.max() - x.time_received_dt.min(), x.time_received_dt.min()]],columns=['diff','min']))
	
	min_training["hour"] = min_training["min"].dt.hour
	min_training = data_processing.hour_break_down(min_training)

	print(type(list(min_training["diff"])[0]))

	min_training["diff_sec"] = min_training["diff"].astype('timedelta64[s]')

	if arr == None:
		hist, arr = pd.qcut(min_training["diff_sec"], 3, retbins= True, duplicates="drop")
	
	min_training["label"] = ""

	min_training.loc[(min_training["diff_sec"] < arr[1]), ["label"]] = "low"
	min_training.loc[((min_training["diff_sec"] < arr[2]) & (min_training["diff_sec"] >= arr[1])), ["label"]] = "medium"
	min_training.loc[(min_training["diff_sec"] >= arr[2]), ["label"]] = "high"

	return training, list(arr)

	


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
		training, testing =  pickle_finder.check_for_training_testing(configs, bus_route, next_stop)

		if training == None:
			training, testing = data_loader_preparer.fake_today_processing(configs,bus_route, next_stop)
			training.to_pickle("training#{}#{}#{}.pickle".format(bus_route, next_stop, configs["fake_today"]))
			testing.to_pickle("testing#{}#{}#{}.pickle".format(bus_route, next_stop, configs["fake_today"]))


		training, arr = transform(training)
		testing, _ = transform(testing, arr)

		modeling.modeling_clf(training, testing)

		


	#mapping.plot_from_tbl(training)




if __name__ == '__main__':
	print("hello world.. traffic is solvable problem")
	main()
	