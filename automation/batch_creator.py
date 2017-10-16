import os



files =  os.listdir("./runner_files")

count = 0
i = 0
list_sbatch = []
for file_name in files:
	list_sbatch.append('sbatch runner_files/{}'.format(file_name))
		

with open('batch_runners/runner_{}.s'.format(i), 'w') as file_handler:
	for item in list_sbatch:
		file_handler.write("{}\n".format(item))
