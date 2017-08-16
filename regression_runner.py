import sys
import yaml
import pickle
import regression_utils


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
		

	regression_utils.iterate_stops(network_training, network_testing)

	#print(network)

if __name__ == '__main__':
	print("hello world... let's not regress...")
	main()