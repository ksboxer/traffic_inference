import pickle

with open('segments_twosegments.pickle','rb') as f:
	segments = pickle.load(f)

stops = {}

for key in segments:
	if key not in stops:
		stops[key] = {}
	for stops in segments[key]:
		if len(stops) > 1:
			for i in range(len(stops)-1):
				if (stops[i], stops[i+1]) not in stops[key]:
					stops[key][(stops[i], stops[i+1])] = 1
				else:
					stops[key][(stops[i], stops[i+1])] = stops[key][(stops[i], stops[i+1])] + 1

with open('stops_two_segments.pickle', 'wb') as f:
	pickle.dump(stops, f, protocol=pickle.HIGHEST_PROTOCOL)