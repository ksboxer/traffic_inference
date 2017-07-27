import os
from datetime import datetime
import data_loader_utils
import data_utils
import pandas as pd
import json
import pickle

def get_agg(configs):
	fake_today = configs["fake_today"]
	files = os.listdir(configs['raw_data_path'])
	segments = {}
	for file in files:
		tbl = data_loader_utils.read_in_table_by_filename(configs,str(file))

		agg_dict = data_utils.aggegrate_data(tbl).to_dict()
		#print(agg_dict)

		for key in agg_dict:
			if key not in segments:
				segments[key] = agg_dict[key]
	return segments



def fake_today_processing(configs, route_id, bus_stop):
	fake_today = configs["fake_today"]
	files = os.listdir(configs['raw_data_path'])
	training = pd.DataFrame()
	testing = pd.DataFrame()

	with open('segments.json', 'w') as fp:
		json.dump(segments, fp)
	
	for file in files:
		file_date = file.replace("MTA-Bus-Time_.", "").replace(".txt", "")
		file_date = datetime.strptime(file_date, '%Y-%m-%d').date()
			
		tbl = data_loader_utils.read_in_table_by_filename(configs,str(file))

		tbl = data_utils.rows_by_routeid_nextstop(tbl, configs, route_id, bus_stop)
		print tbl
		tbl = data_utils.transform(tbl)

		if file_date < fake_today:
			training = training.append(tbl)
		else:
			testing = testing.append(tbl)
	return training, testing