import requests
import pandas as pd
import json
from bigq_extract import query_db

AccountKey="gWSUabRUR9OGSiPqjbSI0g=="

class FacilitiesMaintenanceDAO:
    def __init__(self):
        self.path='./sample_assets/facilitiesMaintenance.csv'
        self.pdTable=None
        query_data = query_db()
        query = "SELECT * FROM `nus-competition.Traffic.facility_maintenance`"
        self.facility_maintenance_df = query_data.run_query(query)
        pass

    def loadFromHTTP(self):
        headers={'AccountKey': AccountKey}
        stationCodeList=pd.read_csv("./sample_assets/Train Station Codes and Chinese Names.csv")['stn_code'].to_list()

        listOfMaintenance=[]
        for code in stationCodeList:

            try:
                params={'StationCode':code}
                response=requests.get("http://datamall2.mytransport.sg/ltaodataservice/FacilitiesMaintenance",params=params,headers=headers)

                url=json.loads(response.text)['value'][0]['Link']
                response=requests.get(url=url,headers=headers)
                jsonObject=json.loads(response.text)

                for item in jsonObject['schedule']:
                    for detail in item['details']:
                        for liftDesc in detail['liftDesc']:
                            table={}
                            table['Station Code']=jsonObject['stationCode']
                            table['Station Name']=jsonObject['stationName']
                            table['Date&Time']=item['maintenanceDt']+" "+detail['maintenanceTime']
                            table['Detail']=liftDesc
                            listOfMaintenance.append(table)
            except:
                pass

        self.pdTable=pd.DataFrame(listOfMaintenance)
        self.pdTable.to_csv(self.path)
    
    def loadFromCSV(self):
        try:
            #self.pdTable=pd.read_csv(self.path)
            self.pdTable=self.facility_maintenance_df
        except:
            print("FacilitiesMaintenanceDAO: FAILED TO LOAD CSV")
        self.pdTable=self.pdTable.filter(items=['Station Code','Station Name','Date&Time','Detail'])
        #self.pdTable=self.pdTable.groupby(['Station Name','Date&Time','Detail']).aggregate('list')

    def getUniqueStationNameList(self):
        list=self.pdTable.groupby("Station Name").aggregate('count').reset_index()['Station Name'].to_list()
        return(list)
    
    def getDataframeByStationName(self,stationName):
        if stationName==None:
            return self.pdTable
        if stationName=="":
            return self.pdTable
        if stationName=="__ALL__":
            return self.pdTable
        
        return self.pdTable[self.pdTable['Station Name']==stationName]