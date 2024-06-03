import pandas as pd
import json
from bigq_extract import query_db

class VolumeByTrainStationDAO:
    def __init__(self):
        self.volumeByTrainStation=None
        query_data = query_db()
        query = "SELECT * FROM `nus-competition.Traffic.transport_node_train`"
        self.transport_node_train_df = query_data.run_query(query)
        pass

    def loadLocalData(self):
        volumeDataframe=self.transport_node_train_df.filter(items=["PT_CODE","TOTAL_TAP_IN_VOLUME","TOTAL_TAP_OUT_VOLUME"]).groupby(["PT_CODE"]).aggregate('sum').reset_index()
        volumeDataframe['stn_code']=volumeDataframe['PT_CODE'].apply(lambda x: x.split('/')[-1])

        trainStationDataframe=pd.read_csv("./sample_assets/Train Station Codes and Chinese Names.csv")

        self.volumeByTrainStation=pd.merge(volumeDataframe,trainStationDataframe,on="stn_code",how="left")