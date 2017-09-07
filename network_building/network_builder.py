import yaml
import sys,os
lib_path = os.path.abspath('./utils')
sys.path.insert(0,lib_path)

import data_loader_utils
from datetime import datetime
import build_network
import pickle
import mapping
from gmplot import GoogleMapPlotter as gmp

def read_in_table(configs, date):
	file = 'MTA-Bus-Time_.'+date+'.txt'
	tbl = data_loader_utils.read_in_table_by_filename(configs,str(file))
	return tbl



def main():
	# reads in configs
	yaml_file_path = sys.argv[1]
	with open(yaml_file_path) as f:
		configs = yaml.load(f)

	dates = [configs['network_date']]
	if len(sys.argv) > 2:
		with open(sys.argv[2]) as fp:
			dates = fp.read().split("\n")
	
	for date in dates:
		data_tbl = read_in_table(configs, date)

		network  = build_network.build(data_tbl)
		build_network.add_time_table(network)
		with open('networks_by_date/network_'+date+'.pickle', 'wb') as f:
			pickle.dump(network, f, protocol=pickle.HIGHEST_PROTOCOL)
		

	'''with open('networks_by_date/network_'+configs['network_date']+'.pickle', 'rb') as f:
		network = pickle.load(f)
	build_network.add_time_table(network)
	with open('networks_by_date/network_'+configs['network_date']+'_with_duration'+'.pickle', 'wb') as f:
		pickle.dump(network, f, protocol=pickle.HIGHEST_PROTOCOL)
	'''
if __name__ == '__main__':
	print("hello network_builder")
	main()