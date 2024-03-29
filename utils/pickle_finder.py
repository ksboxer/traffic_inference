import pickle
import os

def check_for_training_testing(configs, bus_route, next_stop):
	training_path = 'training/training#{}#{}#{}.pickle'.format(bus_route, next_stop, configs["fake_today"])
	testing_path = 'testing/testing#{}#{}#{}.pickle'.format(bus_route, next_stop, configs["fake_today"])
	if os.path.isfile(training_path):
		with open(training_path, "rb") as input_file:
			training = pickle.load(input_file)

		with open(testing_path, "rb") as input_file:
			testing = pickle.load(input_file)
		return training, testing
	else:
		return None, None

def check_training_testing_two_segment(configs, bus_route, stop1, stop2):
	training_path = 'training_twosegments/training#{}#{}#{}#{}.pickle'.format(bus_route, stop1, stop2, configs["fake_today"])
	testing_path = 'testing_twosegments/testing#{}#{}#{}#{}.pickle'.format(bus_route, stop1, stop2, configs["fake_today"])
	if os.path.isfile(training_path):
		with open(training_path, "rb") as input_file:
			training = pickle.load(input_file)

		with open(testing_path, "rb") as input_file:
			testing = pickle.load(input_file)
		return training, testing
	else:
		return None, None
