import pandas as pd
from itertools import groupby
import json
import pickle

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

def transform(tbl):
	return tbl

def add_day_column(tbl):
	tbl["time_received_dt"] = pd.to_datetime(tbl["time_received"])
	tbl["day"] = tbl["time_received_dt"].dt.day
	tbl["month"] = tbl["time_received_dt"].dt.month
	tbl["hour"] = tbl["time_received_dt"].dt.hour
	return tbl