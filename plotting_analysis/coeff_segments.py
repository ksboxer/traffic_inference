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

features =  ["duration_t_minus_10", "duration_t_minus_20", "duration_t_minus_30",
      "duration_t_minus_40", "duration_t_minus_50" , "time_before_6", "time_6_9", "time_9_12", "time_12_16",
      "time_16_19", "time_19_24" , 'sum_segment_duration', 'mean_segment_duration', 'number_segments', 'std_of_segments']


segment_titles = ['mean_segment_duration', 'number_segments',
	'std_of_segments', 'sum_segment_duration']

def sort_coef(cols, coef, error):
	df = pd.DataFrame({'cols': cols, 'coef':coef, 'error': error}, columns = ['cols', 'coef', 'error'])
	df['coef_abs'] = df['coef'].abs()
	df = df[df['coef'] != 0]
	df = df.sort_values(['coef_abs'], ascending= False)
	df = df.reset_index()
	df['index'] = 0
	df['rank'] = df['coef_abs'].rank(ascending= False)
	#print(df)
	return df

def all_zero(lst):
	all_z = True
	for i in lst:
		if i != 0 :
			all_z = False
	return all_z

def df_in_list(df, lst):
	for df_temp in lst:
		if df_temp.equals(df):
			return True
	return False


df_total = pd.DataFrame()
error_dist = []
for filename in glob('regression_results_3/*'):
	if 'classFalse' in filename:
		with open(filename, 'r') as f:
			results = json.load(f)

		res = [] 

		first = True
		for rowKey in results:
			row = results[rowKey]
			stop = row['stop']
			previous_stop = row['previous_stop']
			cols_used = row['cols_used']
			coef = row['coef']
			error = row['error']
			if first:
				error_dist.append(error)
				first = False

			#print('{} {}'.format(previous_stop, stop))
			if all_zero(coef[0]) == False:
				df = sort_coef(cols_used, coef[0], [error]*(len(cols_used)))
				if df_in_list(df, res) == False:
					res.append(df)
					df_total = df_total.append(df)

		if len(res) > 0:
			pass

groups  = df_total.groupby(['cols']).agg({np.sum})
print(groups)
print(list(groups))
print(groups.sort_values(('rank','sum')))
#print(groups['cols'])

for feature in features:
	df_seg = df_total[df_total['cols'] == feature]
	
	plt.figure()
	plt.xlabel(feature + ' coef')
	ax = df_seg['coef'].plot(kind='density')
	fig = ax.get_figure()
	fig.savefig('coef_hist/'+feature+'.png')

for feature in features:
	df_seg = df_total[df_total['cols'] == feature]
	
	plt.figure(figsize= (60,30))
	plt.xlabel(feature + ' coef')
	ax = df_seg.plot('coef','error',kind='scatter', figsize= (30,20), xlim = (-1,1))
	fig = ax.get_figure()
	fig.savefig('coef_error/'+feature+'.png')

plt.figure()
plt.hist(error_dist, bins = 100)
plt.ylabel('count')
plt.xlabel('error (s)')
plt.savefig('error_dist.png')

with open('error_list.txt', 'w') as file_handler:
    for item in error_dist:
        file_handler.write("{}\n".format(item))