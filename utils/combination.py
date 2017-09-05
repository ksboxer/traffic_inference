import pandas as pd
import pickle

import os, sys

lib_path = os.path.abspath('./')
sys.path.insert(0,lib_path)

def combine_list_of_networks(configs,key):
	training_dates = configs[key]
	with open('networks_by_date/network_'+training_dates[0]+'.pickle', 'rb') as f:
		initial_network = pickle.load(f)
	for i in range(1, len(training_dates)):
		print('adding {} to network'.format(training_dates[i]))
		with open('networks_by_date/network_'+training_dates[i]+'.pickle', 'rb') as f:
			temp_network = pickle.load(f)
			initial_network = combine_two_networks(temp_network, initial_network)
	return initial_network

def combine_two_networks(network_1, network_2):
	for stop_1 in network_1.keys():
		if stop_1 not in network_2:
			network_2[stop_1] = network_1[stop_1]
		else:
			for previous_stop_1 in network_1[stop_1].incoming_traffic:
				if previous_stop_1 not in network_2[stop_1].incoming_traffic:
					network_2[stop_1].incoming_traffic[previous_stop_1] = network_1[stop_1].incoming_traffic[previous_stop_1]
				else:
					if 'duration_table' in network_1[stop_1].incoming_traffic[previous_stop_1]:
						if 'duration_table' in network_2[stop_1].incoming_traffic[previous_stop_1]:
							network_2[stop_1].incoming_traffic[previous_stop_1]['duration_table'] = pd.concat([network_2[stop_1].incoming_traffic[previous_stop_1]['duration_table'] , network_1[stop_1].incoming_traffic[previous_stop_1]['duration_table'] ])
						else:
							network_2[stop_1].incoming_traffic[previous_stop_1]['duration_table'] = network_1[stop_1].incoming_traffic[previous_stop_1]['duration_table'] 
	return network_2