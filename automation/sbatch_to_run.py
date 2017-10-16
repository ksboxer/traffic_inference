import os
import json
import pandas as pd

result_folder = './regression_results_3'
runner_folder = './runner_files'

json_files = os.listdir(result_folder)
runner_files = os.listdir(runner_folder)

print(len(runner_files))
#print(json_files)

full_data_class = pd.DataFrame()
full_data_regr = pd.DataFrame()

for file in json_files:
	#print('{}/{}'.format(result_folder, file))
	#with open('{}/{}'.format(result_folder, file), 'r') as fp:
	#	ex = json.load(fp)
		#print(ex)
	temp_df = pd.read_json('{}/{}'.format(result_folder, file), 'index')
	
	if 'accuracy' in list(temp_df):
		full_data_class = full_data_class.append(temp_df)
	else:
		full_data_regr = full_data_regr.append(temp_df)

distinct_class = full_data_class[['previous_stop', 'stop']].drop_duplicates()
distinct_regr = full_data_regr[['previous_stop', 'stop']].drop_duplicates()

for index, row in distinct_class.iterrows():
	runner_file_temp = 'runner_{}_{}_class.s'.format(row['previous_stop'], row['stop'])
	runner_files.remove(runner_file_temp)

for index, row in distinct_regr.iterrows():
	runner_file_temp = 'runner_{}_{}_regr.s'.format(row['previous_stop'], row['stop'])
	runner_files.remove(runner_file_temp)

print(len(runner_files))

final_lines  = []

for row in runner_files:
	final_lines.append('sbatch runner_files/{}'.format(row))

with open('runner_temp.s', 'w') as file_handler:
    for item in final_lines:
        file_handler.write("{}\n".format(item))


