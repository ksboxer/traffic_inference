import data_utils 
import bus_stop

def build(data_tbl):
	network = {}
	# only manhattan
	data_tbl = data_utils.add_manhattan(data_tbl)
	data_tbl = data_tbl.sort_values(["inferred_route_id","inferred_trip_id", "vehicle_id", "time_received"])
	
	groups = data_tbl.groupby(["inferred_route_id","inferred_trip_id", "vehicle_id"])
	
	for (route, trip_id, vehicle_id), group in groups:
		previous_stop = "source_"+route
		stops = group.groupby(["next_scheduled_stop_id"])
		for stop, sample in stops:

			sample["inferred_route_id"] = route
			sample["infered_trip_id"] = trip_id
			sample["vehicle_id"] = vehicle_id

			if stop not in network:
				network[stop] = bus_stop.BusStop(previous_stop, sample)
			else:
				network[stop].add_incoming_link(previous_stop, sample)
			previous_stop = stop
	print network
	return network


	#print data_tbl
