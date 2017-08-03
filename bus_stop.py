import pandas as pd

class BusStop:

	def __init__(self, previous_stop, row):
		self.name = row['next_scheduled_stop_id']
		self.incoming_traffic = {previous_stop: {"raw_data": row}}

	def add_incoming_link(self, previous_stop, row):
		if previous_stop not in self.incoming_traffic:
			self.incoming_traffic[previous_stop] = {}
			self.incoming_traffic[previous_stop]["raw_data"] = row
		else:
			self.incoming_traffic[previous_stop]["raw_data"] = self.incoming_traffic[previous_stop]["raw_data"].append(row)

	def build_time_def_table(self):
		rows = []
		#print(self.incoming_traffic["time_received"])
		for previous_stop in self.incoming_traffic:
			print(self.incoming_traffic[previous_stop])
			self.incoming_traffic[previous_stop]["raw_data"]["time_received_dt"] = pd.to_datetime(self.incoming_traffic[previous_stop]["raw_data"]["time_received"])
			self.incoming_traffic[previous_stop]["raw_data"].sort_values(["inferred_route_id", "inferred_trip_id", "vehicle_id", "time_received"])
			groups = self.incoming_traffic[previous_stop]["raw_data"].groupby(["inferred_route_id", "inferred_trip_id", "vehicle_id"])
			for (inferred_route_id, inferred_trip_id, vehicle_id), group in groups:
				if len(group) > 1:
					print("FIRST")

					start_time = group["time_received_dt"].iloc[0]
					end_time = group["time_received_dt"].iloc[len(group)-1]

					print(len(group))
					print(start_time)
					print(end_time)

					duration = end_time - start_time

					info = (inferred_route_id, inferred_trip_id, vehicle_id, start_time, end_time, duration)
					rows.append(info)

			#print(rows)
			if len(rows) > 1:
				tmp_df = pd.DataFrame(rows, columns=['inferred_route_id', 'inferred_trip_id', 'vehicle_id','start_time', 'end_time', 'duration'])
				self.incoming_traffic[previous_stop]["duration_table"] = tmp_df
				print("added")