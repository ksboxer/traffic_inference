from glob import glob
import json
import os
import pandas as pd

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

means = []
errors = []

for filename in glob('regression_results_3/*.html'):
	if 'classFalse'  in filename:
		with open(filename, 'r') as f:
			results = json.load(f)
		results_sub = results[results.keys()[0]]
		previous_stop = results_sub['previous_stop']
		stop = results_sub['stop']
	
		#means = []
		#errors = []
		if os.path.exists('variation_segments_count/{}_{}.json'.format(previous_stop, stop)) and 'error' in results_sub:
			with open('variation_segments_count/{}_{}.json'.format(previous_stop, stop), 'r') as f:
				variation = json.load(f)
				total = 0
				for k in variation:
					total = total + variation[k]['count']
				mean = total / len(variation)
				print(mean)
				means.append(mean)
				print(results_sub)
				errors.append(results_sub['error'])
#fig = plt.figure()

plt.figure(figsize=(20,30))
plt.scatter(means,errors)
plt.ylabel('errors (s)')
plt.xlabel('rate per hour of bus traversal')
plt.savefig('rate_vs_error.png')

