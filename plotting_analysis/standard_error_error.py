import os, sys
import pickle
import mapping
import pandas as pd


from glob import glob
import json
import numpy as np

lib_path = os.path.abspath('./utils')
sys.path.insert(0,lib_path)

import json

import combination

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

with open('training_full.pickle', 'rb') as f:
	network_training = pickle.load(f)


regrError = []
standardErrors = []

for filename in glob('regression_results_3/*'):
	if 'classFalse' in filename:
		with open(filename, 'r') as f:
			results = json.load(f)

		res = results[results.keys()[0]]
		
		previous_stop = res['previous_stop']
		stop = res['stop']
		error = res['error']

		regrError.append(error)

		duration_table = network_training[stop].incoming_traffic[previous_stop]['duration_table']
		n = len(duration_table)
		duration_table['duration_s'] = duration_table['duration'].astype('timedelta64[s]').astype(int)
		std = duration_table['duration_s'].std()

		standard_error = std / (n**(.5))
		print(float(standard_error))

		standardErrors.append(float(standard_error))


plt.figure(figsize=(30,30))
plt.scatter(regrError,standardErrors)
plt.ylabel('standard error (s)')
plt.xlabel('regression error (s)')
plt.savefig('standard_v_regression.png')

with open('standard_v_regression.txt', 'w') as file_handler:
    for idx,item in enumerate(regrError):
        file_handler.write("{},{}\n".format(item, standardErrors[idx]))