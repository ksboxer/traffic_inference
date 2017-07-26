from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn import tree

def modeling_svm(training, testing):
	pass
	clf = svm.LinearSVC()
	clf.fit(training.loc[:, ["time_before_6", "time_6_9", "time_9_12", "time_12_16", "time_16_19", "time_19_24" ] ], training.loc[:, ["speed_label"]])
	labels = clf.predict(testing.loc[:, ["time_before_6", "time_6_9", "time_9_12", "time_12_16", "time_16_19", "time_19_24" ] ])

	#ACCURACY SCORE 
	#print(list(labels))
	errors = {}
	for i,label in enumerate(labels):
		#print("{} -- {}".format(label, list(testing["speed_label"])[i]))
		if "{} -- {}".format(label, list(testing["speed_label"])[i]) not in errors:
			errors["{} -- {}".format(label, list(testing["speed_label"])[i])] = 1
		else:
			errors["{} -- {}".format(label, list(testing["speed_label"])[i])] = errors["{} -- {}".format(label, list(testing["speed_label"])[i])] +1 
	print(errors)
	print(accuracy_score(testing.loc[:, ["speed_label"]],labels))