import yaml
import pickle
import sys
import mapping


def main():

	yaml_file_path = sys.argv[1]
	with open(yaml_file_path) as f:
		configs = yaml.load(f)

	with open('networks_by_date/network_'+configs['network_date']+'_with_duration'+'.pickle', 'rb') as f:
		network = pickle.load(f)

	for key in network:
		previous_stops = network[key].incoming_traffic.keys()
		network[key].plot_duration("traffic_graph", key)
		for previous_stop in previous_stops:
			raw_data = network[key].incoming_traffic[previous_stop]["raw_data"]
			if len(raw_data) > 20:
				#print(raw_data)
				try:
					mapping.plot_from_tbl_segments(raw_data, previous_stop, key, "mapping_network")
				except IndexError:
					print('catch')



if __name__ == '__main__':
	print("hello stats builder")
	main()