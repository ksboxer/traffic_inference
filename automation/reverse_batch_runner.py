


with open("runner_temp.s", "r") as file:
     my_list = file.readlines()

my_list.reverse()

with open('reverse_temp.s', "w") as f:
	for item in my_list:
  		f.write("%s\n" % item)
