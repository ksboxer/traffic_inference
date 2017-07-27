from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.externals.six import StringIO  
import pydotplus


def modeling_clf(training, testing, bus_route, next_stop):
	pass
	clf = tree.DecisionTreeClassifier()
	clf.fit(training.loc[:, ["time_before_6", "time_6_9", "time_9_12", "time_12_16", "time_16_19", "time_19_24", "weekday" ] ], training.loc[:, ["label"]])
	labels = clf.predict(testing.loc[:, ["time_before_6", "time_6_9", "time_9_12", "time_12_16", "time_16_19", "time_19_24" , "weekday" ] ])

	#ACCURACY SCORE 
	#print(list(labels))
	errors = {}
	testing["predicted_labels"] = labels
	for i,label in enumerate(labels):
		#print("{} -- {}".format(label, list(testing["speed_label"])[i]))
		if "{} -- {}".format(label, list(testing["label"])[i]) not in errors:
			errors["{} -- {}".format(label, list(testing["label"])[i])] = 1
		else:
			errors["{} -- {}".format(label, list(testing["label"])[i])] = errors["{} -- {}".format(label, list(testing["label"])[i])] +1 
	print(errors)
	acc = accuracy_score(testing.loc[:, ["label"]],labels)
	print(acc)

	results = {}
	results["bus_route"] = bus_route
	results["next_stop"] = next_stop
	results["acc"] = acc
	results["errors"] = errors
	#tree.export_graphviz(clf,out_file='tree.dot')  

	#dot_data = StringIO() 
	#tree.export_graphviz(clf, out_file=dot_data) 
	#graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
	#graph.write_pdf("iris.pdf")
	return results