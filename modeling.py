from sklearn import svm
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error
from sklearn import tree
from sklearn.externals.six import StringIO  
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
import pydotplus

def all_models(training, testing, bus_route, bus_stop1, bus_stop2, extension):
	if len(training) == 0:
		return None
	res = {}
	res["bus_route"] = bus_route
	res["stop1"] = bus_stop1
	res["stop2"] = bus_stop2

	#==================================================

	clf = LinearRegression()
	clf.fit(training.loc[:, ["time_before_6", "time_6_9", "time_9_12", "time_12_16", "time_16_19", "time_19_24", "weekday" ] ], training.loc[:, ["diff_sec"]])
	labels = clf.predict(testing.loc[:, ["time_before_6", "time_6_9", "time_9_12", "time_12_16", "time_16_19", "time_19_24", "weekday" ] ])

	error = mean_absolute_error(testing['diff_sec'], labels)
	res["one_segment_error"] = error

	#==================================================

	clf = LinearRegression()
	clf.fit(training.loc[:, ["time_before_6", "time_6_9", 
		"time_9_12", "time_12_16", "time_16_19", "time_19_24", "weekday",
		 "time_before_6"+extension, "time_6_9"+extension, 
		"time_9_12"+extension, "time_12_16"+extension, "time_16_19"+extension, "time_19_24"+extension, "diff_shift_sec"] ], training.loc[:, ["diff_sec"]])

	labels = clf.predict(testing.loc[:, ["time_before_6", "time_6_9", 
		"time_9_12", "time_12_16", "time_16_19", "time_19_24", "weekday",
		 "time_before_6"+extension, "time_6_9"+extension, 
		"time_9_12"+extension, "time_12_16"+extension, "time_16_19"+extension, "time_19_24"+extension, "diff_shift_sec"] ] )
	error = mean_absolute_error(testing['diff_sec'], labels)
	res["two_segment_first_segment_real_time_error"] = error

	#==================================================
	clf = LinearRegression()
	clf.fit(training.loc[:, ["weekday",
		 "time_before_6"+extension, "time_6_9"+extension, 
		"time_9_12"+extension, "time_12_16"+extension, "time_16_19"+extension, "time_19_24"+extension ]], training.loc[:, ["diff_shift_sec"]])
	labels = clf.predict(testing.loc[:, ["weekday",
		 "time_before_6"+extension, "time_6_9"+extension, 
		"time_9_12"+extension, "time_12_16"+extension, "time_16_19"+extension, "time_19_24"+extension ]])
	testing["diff_predict"] = labels
	error = mean_absolute_error(testing["diff_shift_sec"], labels)
	res["first_segment_error"] = error

	#===================================================
	clf = LinearRegression()
	clf.fit(training.loc[:, ["time_before_6", "time_6_9", 
		"time_9_12", "time_12_16", "time_16_19", "time_19_24", "weekday",
		 "time_before_6"+extension, "time_6_9"+extension, 
		"time_9_12"+extension, "time_12_16"+extension, "time_16_19"+extension, "time_19_24"+extension, "diff_shift_sec"] ], training.loc[:, ["diff_sec"]])

	labels = clf.predict(testing.loc[:, ["time_before_6", "time_6_9", 
		"time_9_12", "time_12_16", "time_16_19", "time_19_24", "weekday",
		 "time_before_6"+extension, "time_6_9"+extension, 
		"time_9_12"+extension, "time_12_16"+extension, "time_16_19"+extension, "time_19_24"+extension, "diff_predict"] ] )
	error = mean_absolute_error(testing['diff_sec'], labels)
	res["all_predicted_test"] = error

	return res

def modeling_clf(training, testing, bus_route, next_stop):
	clf = LinearRegression()
	clf.fit(training.loc[:, ["time_before_6", "time_6_9", "time_9_12", "time_12_16", "time_16_19", "time_19_24", "weekday" ] ], training.loc[:, ["diff_sec"]])
	labels = clf.predict(testing.loc[:, ["time_before_6", "time_6_9", "time_9_12", "time_12_16", "time_16_19", "time_19_24", "weekday" ] ])

	#ACCURACY SCORE 
	#print(list(labels))
	
	testing["predicted_labels"] = labels
	error = mean_absolute_error(testing['diff_sec'], testing['predicted_labels'])
	print(error)

	results = {}
	results["bus_route"] = bus_route
	results["next_stop"] = next_stop
	results["error"] = error
	#tree.export_graphviz(clf,out_file='tree.dot')  

	#dot_data = StringIO() 
	#tree.export_graphviz(clf, out_file=dot_data) 
	#graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
	#graph.write_pdf("iris.pdf")
	return results