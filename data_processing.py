import numpy as np
import pandas as pd
from datetime import datetime



def week_day(tbl):
	tbl["weekday"] = 0
	print(tbl)
	#df[df['inferred_trip_id'].str.contains("Weekday")]
	tbl.loc[tbl['inferred_trip_id'].str.contains("Weekday"),["weekday"]] = 1
	return tbl

def hour_break_down(tbl):
	tbl["time_before_6"] = (tbl["hour"] <6).astype(int)
	tbl["time_6_9"] = ((tbl["hour"] >= 6) & (tbl["hour"] < 9)).astype(int)
	tbl["time_9_12"] = ((tbl["hour"] >= 9) & (tbl["hour"] < 12)).astype(int)
	tbl["time_12_16"] = ((tbl["hour"] >= 12) & (tbl["hour"] < 16 )).astype(int)
	tbl["time_16_19"] = ((tbl["hour"] >= 16) & (tbl["hour"] < 19 )).astype(int)
	tbl["time_19_24"] = ((tbl["hour"] >= 19) & (tbl["hour"] < 24 )).astype(int)
	return tbl


def table_processing_training(tbl):
	tbl["time_received_datetime"] = pd.to_datetime(tbl["time_received"])
	tbl["time_hour"] = tbl["time_received_datetime"].dt.hour

	tbl["time_before_6"] = (tbl["time_hour"] <6).astype(int)
	tbl["time_6_9"] = ((tbl["time_hour"] >= 6) & (tbl["time_hour"] < 9)).astype(int)
	tbl["time_9_12"] = ((tbl["time_hour"] >= 9) & (tbl["time_hour"] < 12)).astype(int)
	tbl["time_12_16"] = ((tbl["time_hour"] >= 12) & (tbl["time_hour"] < 16 )).astype(int)
	tbl["time_16_19"] = ((tbl["time_hour"] >= 16) & (tbl["time_hour"] < 19 )).astype(int)
	tbl["time_19_24"] = ((tbl["time_hour"] >= 19) & (tbl["time_hour"] < 24 )).astype(int)

	tbl["waiting"] = (tbl["distance_along_trip"] - tbl["distance_along_trip_shift"] ==0).astype(int)
	hist, arr = pd.qcut(tbl["speed"], 3, retbins= True, duplicates="drop")
	tbl["speed_label"] = ""
	print arr


	tbl.loc[tbl["speed"] <= arr[0], ["speed_label"]] = "low"
	tbl.loc[((tbl["speed"] <= arr[1]) & (tbl["speed"] > arr[0])), ["speed_label"]] = "medium"
	tbl.loc[((tbl["speed"] > arr[1])), ["speed_label"]] = "high" 
	tbl = tbl.loc[:, ["time_before_6", "time_6_9", "time_9_12", "time_12_16", "time_16_19", "time_19_24", "waiting", "speed_label"]]
	return tbl, arr

def table_processing_testing(tbl, arr):
	tbl["time_received_datetime"] = pd.to_datetime(tbl["time_received"])
	tbl["time_hour"] = tbl["time_received_datetime"].dt.hour

	tbl["time_before_6"] = (tbl["time_hour"] <6).astype(int)
	tbl["time_6_9"] = ((tbl["time_hour"] >= 6) & (tbl["time_hour"] < 9)).astype(int)
	tbl["time_9_12"] = ((tbl["time_hour"] >= 9) & (tbl["time_hour"] < 12)).astype(int)
	tbl["time_12_16"] = ((tbl["time_hour"] >= 12) & (tbl["time_hour"] < 16 )).astype(int)
	tbl["time_16_19"] = ((tbl["time_hour"] >= 16) & (tbl["time_hour"] < 19 )).astype(int)
	tbl["time_19_24"] = ((tbl["time_hour"] >= 19) & (tbl["time_hour"] < 24 )).astype(int)
	

	tbl["waiting"] = (tbl["distance_along_trip"] - tbl["distance_along_trip_shift"] == 0).astype(int)

	tbl["speed_label"] = ""


	

	tbl.loc[tbl["speed"] <= arr[0], ["speed_label"]] = "low"
	tbl.loc[((tbl["speed"] <= arr[1]) & (tbl["speed"] > arr[0])), ["speed_label"]] = "medium"
	tbl.loc[((tbl["speed"] > arr[1])), ["speed_label"]] = "high" 
	tbl = tbl.loc[:, ["time_before_6", "time_6_9", "time_9_12", "time_12_16", "time_16_19", "time_19_24","waiting", "speed_label"]]
	
	return tbl

