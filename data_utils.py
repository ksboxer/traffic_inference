import pandas as pd
from itertools import groupby
import json
import pickle
import numpy as np

def add_manhattan(tbl):
	tbl["inferred_route_id"] = tbl["inferred_route_id"].fillna("none")
	tbl = tbl[tbl['inferred_route_id'].str.contains("MTA NYCT_M")]
	return tbl


def aggegrate_data(tbl):
	#print(tbl)
	agg_tbl = tbl.groupby(["inferred_route_id", "next_scheduled_stop_id"]).count()
	return agg_tbl

def aggegrate_data_twosegments(tbl):
	tbl  = tbl.sort_values (["time_received"])
	tbl = add_manhattan(tbl)
	agg_tbl = tbl.groupby(["inferred_route_id", "inferred_trip_id","vehicle_id"]).apply(lambda x: x.to_dict(orient='records'))
	
	segments = {}

	for group in agg_tbl:
		group_df = pd.DataFrame(group)
		group_df  = group_df.sort_values (["time_received"])
		#print(group_df)
		if (group_df.loc[0, 'inferred_route_id'], group_df.loc[0, 'inferred_trip_id']) in segments:
			if [x[0] for x in groupby(group_df["next_scheduled_stop_id"].tolist())]  not in segments[(group_df.loc[0, 'inferred_route_id'], group_df.loc[0, 'inferred_trip_id'])]:
				segments[(group_df.loc[0, 'inferred_route_id'], group_df.loc[0, 'inferred_trip_id'])].append([x[0] for x in groupby(group_df["next_scheduled_stop_id"].tolist())])
		else:
			segments[(group_df.loc[0, 'inferred_route_id'], group_df.loc[0, 'inferred_trip_id'])] = [[x[0] for x in groupby(group_df["next_scheduled_stop_id"].tolist())]]

	return segments

def rows_by_routeid_nextstop(tbl,route_id, bus_stop):
	tbl= tbl[tbl["inferred_route_id"] == route_id]
	tbl = tbl[tbl["next_scheduled_stop_id"] == bus_stop]
	return tbl

def rows_by_routeid_nextstop_twosegments(tbl, route_id, bus_stop1, bus_stop2):
	tbl = tbl[tbl["inferred_route_id"] == route_id]
	tbl = tbl.sort_values(["vehicle_id",  "inferred_trip_id", "time_received"])
	tbl["inferred_trip_id_c"] = tbl["inferred_trip_id"]
	tbl["next_scheduled_stop_id_c"] = tbl["next_scheduled_stop_id"]
	tbl["vehicle_id_c"] = tbl["vehicle_id"]
	tbl = add_day_column(tbl)
	tbl = tbl.sort_values(["vehicle_id",  "inferred_trip_id", "time_received_dt"])
	temp = tbl.groupby(["vehicle_id","inferred_trip_id","next_scheduled_stop_id"], group_keys = False).apply(lambda x: pd.DataFrame([[x.vehicle_id_c.iloc[0], x.time_received_dt.max() - x.time_received_dt.min(), x.time_received_dt.min(), x.inferred_trip_id_c.iloc[0],  x.time_received_dt.max(), x.next_scheduled_stop_id_c.iloc[0]]],columns=['vehicle_id','diff','min', "inferred_trip_id",  "max","next_scheduled_stop_id"]))
	temp["next_scheduled_stop_shift"] = temp["next_scheduled_stop_id"].shift(1)
	temp["max_shift"] = temp["max"].shift(1)
	temp["min_shift"] = temp["min"].shift(1)
	temp["diff_shift"] = temp["diff"].shift(1)

	temp["vehicle_id_shift"] = temp["vehicle_id"].shift(1)
	temp["inferred_trip_id_shift"] = temp["inferred_trip_id"].shift(1)
	#temp["next_scheduled_stop_id_shift"] = temp["next_scheduled_stop_id"].shift(1)

	temp = temp[temp["vehicle_id_shift"] == temp["vehicle_id"]]
	temp = temp[temp["inferred_trip_id_shift"] == temp["inferred_trip_id"]]

	temp = temp[temp["max"] > temp["max_shift"]]
	temp = temp[temp["min"] > temp["min_shift"]]
	temp = temp[(temp["next_scheduled_stop_id"] == bus_stop2) & (temp["next_scheduled_stop_shift"] == bus_stop1)]
	#print(temp)
	#tbl["next_bus_shift"] = tbl["next_scheduled_stop_id"].shift(1)

	#print(tbl[(tbl["next_scheduled_stop_id"] == bus_stop2) & (tbl["next_bus_shift"] == bus_stop1)])
	#print(tbl)
	return temp


def transform(tbl):
	return tbl

def add_day_column(tbl, key="time_received"):
	tbl["time_received_dt"] = pd.to_datetime(tbl[key])
	tbl["day"] = tbl["time_received_dt"].dt.day.apply(str)
	tbl["month"] = tbl["time_received_dt"].dt.month.apply(str)
	tbl["hour"] = tbl["time_received_dt"].dt.hour.apply(str)
	tbl["min"] = tbl["time_received_dt"].dt.minute
	return tbl

def add_thirty_min_columns(tbl):
	tbl["thirty_min"] = 0
	tbl["thirty_min"] = np.where(tbl["min"] < 31, "less than 30", "more than 30")
	return tbl