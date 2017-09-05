import yaml
import sys
sys.path.append('..')
import data_loader_utils
from datetime import datetime
import build_network
import pickle
import mapping
from gmplot import GoogleMapPlotter as gmp

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
	'''gmap = gmp.from_geocode("New York City")
	gmap.scatter(data_tbl['latitude'], data_tbl['longitude'], '#3B0B39', size=5, marker=False)
	#gmap.plot(list(tbl['latitude']), tbl['longitude'], 'cornflowerblue', edge_width=10)
	map_file_name = "full_coverage.html"
	gmap.draw(map_file_name)
	mapper.add_key(map_file_name)'''
	#print(data_tbl)
	network  = build_network.build(data_tbl)
	build_network.add_time_table(network)
	with open('networks_by_date/network_'+configs['network_date']+'.pickle', 'wb') as f:
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