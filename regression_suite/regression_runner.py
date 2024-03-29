import sys
import yaml
import pickle
import regression_utils

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import os, sys

lib_path = os.path.abspath('./utils')
sys.path.insert(0,lib_path)

import combination
import json
import pandas as pd
pd.set_option('display.max_colwidth', -1)

import time
import regression_features


def read_in_table(configs):
	file = 'MTA-Bus-Time_.'+configs['network_date']+'.txt'
	tbl = data_loader_utils.read_in_table_by_filename(configs,str(file))
	return tbl

def main():

	yaml_file_path = sys.argv[1]
	with open(yaml_file_path) as f:
		configs = yaml.load(f)

	print(configs)


	with open('training_full.pickle', 'rb') as f:
		network_training = pickle.load(f)

	with open('testing_full.pickle', 'rb') as f:
		network_testing = pickle.load(f)


	'''network_training = combination.combine_list_of_networks(configs, 'training_dates')

	print('saving training')
	with open('training_full.pickle', 'wb') as handle:
		pickle.dump(network_training, handle, protocol=pickle.HIGHEST_PROTOCOL)


	network_testing = combination.combine_list_of_networks(configs, 'testing_dates')

	print('saving testing')
	with open('testing_full.pickle', 'wb') as handle:
		pickle.dump(network_testing, handle, protocol=pickle.HIGHEST_PROTOCOL)'''

	
	#regression_utils.iterate_stops(network_training, network_testing)
	#color = 'bgrmckg'
	total = []
	cor_tol = []
	features_set = regression_features.generate_features_from_configs(configs)
	for idx, previous_stop in enumerate(configs['previous_stop_list']):
		stop = configs['stop_list'][idx]
		info, cor_info =  regression_utils.run_configs_stops(network_training, network_testing, stop, previous_stop, configs, features_set, True, configs["classification"])
		if info != None:
			total = total + info
		if cor_info != None:
			cor_tol = cor_tol + cor_info
		'''points_point_x = list(info.keys())
		points_point_y = []
		#print(info)
		for p in points_point_x:
			points_point_y.append(info[p]['error']/ info[p]['mean'])
		print(stop)
		print(points_point_x)
		print(points_point_y)
		print(info)
		plt.plot(points_point_x, points_point_y, color[idx]+'-')'''

	#plt.savefig('saved_lakshmi_2.png')

	#print(network)

	mins = pd.DataFrame()
	df = pd.DataFrame(total)
	print(df)
	print(list(df))
	groups = df.groupby(['stop','previous_stop'], as_index = False,group_keys = False)
	for name, group in groups:
		if configs["classification"]:
			min_percent = group['accuracy'].max()
			print(min_percent)
			print(group[group['accuracy'] == min_percent])
			mins =mins.append(group[group['accuracy'] == min_percent])
		else:
			min_percent = group['mape'].min()
                        print(min_percent)
                        print(group[group['mape'] == min_percent])
                        mins =mins.append(group[group['mape'] == min_percent])
	
	html = mins.to_json(orient='index')
	print(html)
	ts = time.time()
	with open('regression_results_3/res_class'+str(configs['classification'])+'_'+str(ts)+'.html', "w") as file:
		file.write(html)

	df = pd.DataFrame(cor_tol)
	html = mins.to_json(orient='index')
	html = df.to_html()
	print(html)
	ts = time.time()
	with open('correlation_stats_3/cor'+str(ts)+'.html', "w") as file:
		file.write(html)


if __name__ == '__main__':
	print("hello world... let's not regress...")
	main()
