import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#import seaborn as sns
import matplotlib.dates as mdates
import numpy as np
import time
import os, sys

lib_path = os.path.abspath('utils')
sys.path.insert(0,lib_path)

import data_utils
import json

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
			if len(rows) > 0:
				tmp_df = pd.DataFrame(rows, columns=['inferred_route_id', 'inferred_trip_id', 'vehicle_id','start_time', 'end_time', 'duration'])
				self.incoming_traffic[previous_stop]["duration_table"] = tmp_df
				print("added")

	def plot_duration(self, folder, stop):
		for previous_stop in self.incoming_traffic:
			if "duration_table" in self.incoming_traffic[previous_stop]:
				duration_tbl = self.incoming_traffic[previous_stop]["duration_table"]
				duration_tbl["duration_seconds"] = duration_tbl["duration"].dt.total_seconds()
				#duration_tbl["time"] = pd.to_datetime(duration_tbl['start_time'], format='%Y-%m-%d %H:%M:%S')
				#duration_tbl.set_index(['time'],inplace=True)
				#duration_tbl["time"] = duration_tbl["start_time"].astype(np.int64)
				duration_tbl = duration_tbl.sort_values(['start_time'])
				fig, ax = plt.subplots(figsize=(16,8))
				xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
				ax.xaxis.set_major_formatter(xfmt)
# automatically rotates the tick labels
				fig.autofmt_xdate()

				ax.plot(duration_tbl['start_time'], duration_tbl['duration_seconds'], '-o')
				plt.show()
				#duration_tbl.plot(x="time", y= "duration_seconds")
				#print(duration_tbl)
				#sns.tsplot(data = duration_tbl, time = 'start_time', value = "duration_seconds",  unit="subject")
				#plt.show()
				#print('saving graph')
				plt.savefig('{}/graph#{}#{}.png'.format(folder,  previous_stop, stop))
				time.sleep(1)
				#fig = plot.get_figure()
				#fig.savefig('{}/graph#{}#{}.png'.format(folder, self.name, previous_stop))
	
	def add_stats(self, folder, stop):
		for previous_stop in self.incoming_traffic:
			if "duration_table" in self.incoming_traffic[previous_stop]:
				duration_tbl = self.incoming_traffic[previous_stop]["duration_table"]

				duration_tbl = data_utils.add_day_column(duration_tbl, "start_time")
				duration_tbl  = data_utils.add_thirty_min_columns(duration_tbl)
				#print(duration_tbl)

				duration_tbl = duration_tbl.sort_values(["vehicle_id", "start_time"])

				agg = duration_tbl.groupby([ "month", "day"])

				stats = {}
				stats["days_agg"] = {}
				stats["days_hour_agg"]={}
				stats["days_thirty_min"] = {}

				for (month, day), group in agg:
					#print(month, day)
					#print(len(group))
					stats["days_agg"][str(month)+'_'+str(day)] = len(group)

				agg = duration_tbl.groupby([ "month", "day", "hour"])
				for (month, day, hour), group in agg:
					#print(month, day)
					#print(len(group))
					if str(month)+'_'+day not in stats["days_hour_agg"]:
						stats["days_hour_agg"][str(month)+'_'+str(day)] = {}

					stats["days_hour_agg"][month+'_'+day][hour] = len(group)

				agg = duration_tbl.groupby([ "month", "day", "hour", "thirty_min"])

				for (month, day, hour, thirty), group in agg:
					if month+'_'+day not in stats["days_thirty_min"]:
						stats["days_thirty_min"][month+'_'+day] = {}
					if hour not in stats["days_thirty_min"][month+'_'+day]:
						stats["days_thirty_min"][month+'_'+day][hour] = {}
					stats["days_thirty_min"][month+'_'+day][hour][thirty] = len(group)

				print stats

				with open('{}/{}#{}.json'.format(folder, previous_stop, stop),'w') as f:
					json.dump(stats, f)


				#
				#raw_data = data_utils.add_thirty_min_columns(raw_data)
				#raw_data.sort_values(["vehicle_id", "time_received"])
				#agg = raw_data.groupby(["inferred_route_id", "inferred_trip_id", "vehicle_id", "day", "hour"]).agg(["count"])
				#print(agg)'''
				
