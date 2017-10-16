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

full_mean = []
full_std = []

for filename in glob('variation_segments_count/*'):
	with open(filename, 'r') as f:
		results = json.load(f)

		sum_duration = []
		sum_std = []
		for timeframe in results:
			sum_duration = sum_duration + [results[timeframe]['mean']]*(results[timeframe]['count'])
			#sum_duration.append()
			sum_std.append(results[timeframe]['std'])
        	#sum_duration = sum_duration + results[timeframe]['mean']
        	#sum_std a.results[timeframe]['std']

		
		sum_duration = sum(sum_duration) / len(sum_duration)
		print('mean: {}'.format(sum_duration))
		
		sum_std = filter(lambda a: np.isnan(a) == False, sum_std)
		sum_std = sum(sum_std)/ len(results)
		print('std: {}'.format(sum_std))

       	full_mean.append(sum_duration)
       	full_std.append(sum_std)


plt.figure()
plt.hist(full_mean, bins = 50)
plt.ylabel('duration count')
plt.xlabel('duration (s)')
plt.savefig('mean_duration_histogram.png')

plt.figure()
plt.hist(full_std, bins = 50)
plt.ylabel('duration std count')
plt.xlabel('duration std per segment (s)')
plt.savefig('variation_duration_histogram.png')
             