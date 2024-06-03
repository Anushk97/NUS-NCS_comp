import pandas as pd
from bigq_extract import query_db

class RoadWorksDAO:
    def __init__(self):
        self.roadWorks=None
        query_data = query_db()
        query = "SELECT * FROM `nus-competition.Traffic.road_works`"
        self.road_works_df = query_data.run_query(query)
    
    def loadLocalData(self):
        self.roadWorks=self.road_works_df.drop(labels=["EventID","Other"],axis=1).reindex(columns=["RoadName","SvcDept","StartDate","EndDate"])

    def getUniqueRoadNameList(self):
        list=self.roadWorks.groupby("RoadName").aggregate('count').reset_index()['RoadName'].tolist()
        return(list)
    
    def getDataframeByRoadName(self,roadName):
        if roadName==None:
            return self.roadWorks
        if roadName=="":
            return self.roadWorks
        if roadName=="__ALL__":
            return self.roadWorks
        
        return self.roadWorks[self.roadWorks['RoadName']==roadName]