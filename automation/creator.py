import yaml
import pickle
import pandas as pd
import io

sample_file = """#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=23
#SBATCH --mem=64GB
#SBATCH --job-name=myTest
#SBATCH --mail-type=END
#SBATCH --mail-user=kb145@nyu.edu
#SBATCH --time=48:00:00

module purge
module load anaconda2/4.3.1
python regression_suite/regression_runner.py"""

with open('training_full.pickle', 'rb') as fp:
        training = pickle.load(fp)

with open('testing_full.pickle', 'rb') as fp:
        testing = pickle.load(fp)

with open("configs_400515_400518.yaml", 'r') as stream:
        sample = yaml.load(stream)

for bus_stop in training.keys():
        for previous_stop in training[bus_stop].incoming_traffic:
		if bus_stop in testing and previous_stop in testing[bus_stop].incoming_traffic and 'duration_table' in training[bus_stop].incoming_traffic[previous_stop] and 'duration_table' in testing[bus_stop].incoming_traffic[previous_stop]:
                	print('{},{}'.format(previous_stop, bus_stop))
                	sample['previous_stop_list'] = [previous_stop]
                	sample['stop_list'] = [bus_stop]
                	sample['classification'] = True
                	with io.open('configs_files/configs-{}-{}-{}.yaml'.format(previous_stop, bus_stop, "class"), 'w', encoding='utf8') as outfile:
                        	yaml.dump(sample, outfile, default_flow_style=False, allow_unicode=True)
                	sample_file_class = sample_file + " "+ 'configs_files/configs-{}-{}-{}.yaml'.format(previous_stop, bus_stop, "class")
			with open('runner_files/runner_{}_{}_{}.s'.format(previous_stop, bus_stop, "class"), 'w') as f:
				f.write(sample_file_class) 

			sample['classification'] = False
                	with io.open('configs_files/configs-{}-{}-{}.yaml'.format(previous_stop, bus_stop, "regr"), 'w', encoding='utf8') as outfile:
                        	yaml.dump(sample, outfile, default_flow_style=False, allow_unicode=True)
		
			sample_file_class = sample_file + " "+ 'configs_files/configs-{}-{}-{}.yaml'.format(previous_stop, bus_stop, "regr")

			with open('runner_files/runner_{}_{}_{}.s'.format(previous_stop, bus_stop, "regr"), 'w') as f:
                        	f.write(sample_file_class)
                	print('WROTE')
