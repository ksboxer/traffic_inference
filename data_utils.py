import pandas as pd

def aggegrate_data(tbl):
	#print(tbl)
	agg_tbl = tbl.groupby(["inferred_route_id", "next_scheduled_stop_id"]).count()
	return agg_tbl

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