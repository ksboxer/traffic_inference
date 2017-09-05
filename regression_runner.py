import sys
import yaml
import pickle
import regression_utils

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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



	network_training = combination.combine_list_of_networks(configs, 'training_dates')


	network_testing = combination.combine_list_of_networks(configs, 'testing_dates')

	#regression_utils.iterate_stops(network_training, network_testing)
	#color = 'bgrmckg'
	total = []
	features_set = regression_features.generate_features_from_configs(configs)
	for idx, previous_stop in enumerate(configs['previous_stop_list']):
		stop = configs['stop_list'][idx]
		info =  regression_utils.run_configs_stops(network_training, network_testing, stop, previous_stop, configs, features_set)
		if info != None:
			total = total + info
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
	groups = df.groupby(['stop','previous_stop'], as_index = False,group_keys = False)
	for name, group in groups:
		min_percent = group['error_percent'].min()
		print(min_percent)
		print(group[group['error_percent'] == min_percent])
		mins =mins.append(group[group['error_percent'] == min_percent])
	
	html = mins.to_html()
	print(html)
	ts = time.time()
	with open('regression_results_2/res'+str(ts)+'.html', "w") as file:
		file.write(html)

if __name__ == '__main__':
	print("hello world... let's not regress...")
	main()