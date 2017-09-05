import os
import pandas as pd

def read_in_file_by_date(file):
	files = os.listdir(configs['raw_data_path'])
	for file in files:
		if configs['date'] in file:
			tbl =pd.read_table("{}//{}".format(configs['raw_data_path'], file))
			return tbl

def read_in_table_by_filename(configs, file_name):
	print(file_name)
	tbl =pd.read_table("{}/{}".format(configs['raw_data_path'], file_name))
	return tbl
