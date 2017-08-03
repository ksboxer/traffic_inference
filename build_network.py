import data_utils 
import bus_stop

def build(data_tbl):
	network = {}
	# only manhattan
	data_tbl = data_utils.add_manhattan(data_tbl)
	data_tbl = data_tbl.sort_values(["inferred_route_id","inferred_trip_id", "vehicle_id", "time_received"])
	
	data_tbl["inferred_route_id_c"] = data_tbl["inferred_route_id"]
	data_tbl["inferred_trip_id_c"] = data_tbl["inferred_trip_id"]
	data_tbl["vehicle_id_c"] = data_tbl["vehicle_id"]

	groups = data_tbl.groupby(["inferred_route_id","inferred_trip_id", "vehicle_id"])
	
	for (route, trip_id, vehicle_id), group in groups:
		previous_stop = "source_"+route

		#group["inferred_route_id"] = route
		#group["inferred_trip_id"] = trip_id
		#group["vehicle_id"] = vehicle_id

		stops = group.groupby(["next_scheduled_stop_id"])

		for stop, sample in stops:

			if stop not in network:
				network[stop] = bus_stop.BusStop(previous_stop, sample)
			else:
				network[stop].add_incoming_link(previous_stop, sample)
			previous_stop = stop
	#print network
	return network

def add_time_table(network):
	for stop in network:
		for previous_stop in network[stop].incoming_traffic:
			traffic_data = network[stop].incoming_traffic[previous_stop]
			#print(traffic_data)
			network[stop].build_time_def_table()


	#print data_tbl
