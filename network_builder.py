import yaml
import sys
import data_loader_utils
from datetime import datetime
import build_network
import pickle

def read_in_table(configs):
	file = 'MTA-Bus-Time_.'+configs['network_date']+'.txt'
	tbl = data_loader_utils.read_in_table_by_filename(configs,str(file))
	return tbl



def main():
	# reads in configs
	yaml_file_path = sys.argv[1]
	with open(yaml_file_path) as f:
		configs = yaml.load(f)
	
	data_tbl = read_in_table(configs)
	#print(data_tbl)
	'''network  = build_network.build(data_tbl)
	with open('networks_by_date/network_'+configs['network_date']+'.pickle', 'wb') as f:
		pickle.dump(network, f, protocol=pickle.HIGHEST_PROTOCOL)'''
	

	with open('networks_by_date/network_'+configs['network_date']+'.pickle', 'rb') as f:
		network = pickle.load(f)
	build_network.add_time_table(network)
	with open('networks_by_date/network_'+configs['network_date']+'_with_duration'+'.pickle', 'wb') as f:
		pickle.dump(network, f, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
	print("hello network_builder")
	main()