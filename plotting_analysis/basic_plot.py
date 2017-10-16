import json
import random
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as  plt
import numpy as np

plt.rcParams["figure.figsize"] = [16,9]


with open("for_plot.txt") as file:
	lines = [line.strip() for line in file]

idx = 0
x_one_segment = []
y_one_segment = []

x_all_segments = []
y_all_segments = []

x_previous_segments = []
y_previous_segments = []
lines = random.sample(lines,25)
for json_file in lines:
	with open(json_file, 'r') as f:
		data = json.load(f)
		y_one_segment.append(data['one_segment']['error'] / data['one_segment']['label_mean'])
		x_one_segment.append(idx)

		if 'combined_all_previous_segments' in data:
				y_all_segments.append(data['combined_all_previous_segments']['error'] / data['one_segment']['label_mean'])
				x_all_segments.append(idx)

		if 'previous_segments' in data:
			for segment in data['previous_segments']:
				y_previous_segments.append(data['previous_segments'][segment]['error'] / data['one_segment']['label_mean'])
				x_previous_segments.append(idx)

		idx = idx +1


plt.scatter(x_one_segment, y_one_segment, marker = '^', s=50)
plt.scatter(x_all_segments, y_all_segments, marker = '*', s=50)
plt.scatter(x_previous_segments, y_previous_segments, marker = 'o', s=10)
plt.savefig('example_plt.png')
print(y_previous_segments)