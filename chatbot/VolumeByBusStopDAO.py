import pandas as pd
import json
from bigq_extract import query_db

class VolumeByBusStopDAO:
    def __init__(self):
        self.volumeByBusStop=None
        query_data = query_db()
        
        query = "SELECT * FROM `nus-competition.Traffic.transport_node_bus`"
        self.transport_node_bus_df = query_data.run_query(query)
        self.transport_node_bus_df['PT_CODE'] = self.transport_node_bus_df['PT_CODE'].astype(str)
        
        query2 = "SELECT * FROM `nus-competition.Traffic.bus_stops`"
        self.bus_stops_df = query_data.run_query(query2)
        self.bus_stops_df['BusStopCode'] = self.bus_stops_df['BusStopCode'].astype(str)
        
        pass

    def loadLocalData(self):
        volumeDataframe=pd.read_csv("./sample_assets/transport_node_bus_202402.csv", converters={'PT_CODE':str}).filter(items=["PT_CODE","TOTAL_TAP_IN_VOLUME","TOTAL_TAP_OUT_VOLUME"]).groupby(["PT_CODE"]).aggregate('sum')
        
        volumeDataframe=self.transport_node_bus_df.filter(items=["PT_CODE","TOTAL_TAP_IN_VOLUME","TOTAL_TAP_OUT_VOLUME"]).groupby(["PT_CODE"]).aggregate('sum')

        # with open("./sample_assets/bus_stops.json","r") as f:
        #     jsonObject=json.load(f)

        #busStopDataframe=pd.DataFrame(jsonObject['value']).rename(columns={'BusStopCode':'PT_CODE'})
        busStopDataframe=self.bus_stops_df.rename(columns={'BusStopCode':'PT_CODE'})

        self.volumeByBusStop=pd.merge(busStopDataframe,volumeDataframe,on='PT_CODE',how="left")