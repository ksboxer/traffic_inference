import pickle

def check_for_training_testing(configs, bus_route, next_stop):
	training_path = 'training#{}#{}#{}.pickle'.format(bus_route, next_stop, configs["fake_today"])
	testing_path = 'testing#{}#{}#{}.pickle'.format(bus_route, next_stop, configs["fake_today"])
	if os.path.isfile(training_path):
		with open(training_path, "rb") as input_file:
			training = pickle.load(input_file)

		with open(testing_path, "rb") as input_file:
			testing = pickle.load(input_file)
		return training, testing
	else:
		return None, None