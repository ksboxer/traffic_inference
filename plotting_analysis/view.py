import pickle
import pandas as pd

with open('whole_data.json', 'rb') as f:
	data = pickle.load(f)

#print(data)

df = pd.DataFrame.from_records(data['data'])
df = df.sort_values(['error_percent'])

idx = df.groupby(['stop','previous_stop'], as_index = False,group_keys = False)['error_percent'].idxmin()
print(list(df.loc[idx]['cols_used']))
print(list(df.loc[idx]['coef']))
