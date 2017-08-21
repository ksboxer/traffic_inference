import sys
import yaml
import pickle
import regression_utils

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def read_in_table(configs):
	file = 'MTA-Bus-Time_.'+configs['network_date']+'.txt'
	tbl = data_loader_utils.read_in_table_by_filename(configs,str(file))
	return tbl

def main():

	yaml_file_path = sys.argv[1]
	with open(yaml_file_path) as f:
		configs = yaml.load(f)

	print(configs)

	with open('networks_by_date/network_'+configs['training_date']+'_with_duration'+'.pickle', 'rb') as f:
		network_training = pickle.load(f)

	with open('networks_by_date/network_'+configs['testing_date']+'_with_duration'+'.pickle', 'rb') as f:
		network_testing = pickle.load(f)
		

	#regression_utils.iterate_stops(network_training, network_testing)
	color = 'bgrmck'
	for idx, previous_stop in enumerate(configs['previous_stop_list']):
		stop = configs['stop_list'][idx]
		info =  regression_utils.run_configs_stops(network_training, network_testing, stop, previous_stop)
		points_point_x = list(info.keys())
		points_point_y = []
		print(info)
		for p in points_point_x:
			points_point_y.append(info[p]['error']/ info[p]['mean'])
		print(points_point_x)
		print(points_point_y)
		plt.plot(points_point_x, points_point_y, color[idx]+'-')

	plt.savefig('saved_lakshmi_2.png')

	#print(network)

if __name__ == '__main__':
	print("hello world... let's not regress...")
	main()