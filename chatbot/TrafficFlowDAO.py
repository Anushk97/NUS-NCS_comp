import plotly.graph_objects as go
import plotly.express as px
import json
import pandas as pd
from bigq_extract import query_db
from datetime import datetime

class TrafficFlowDAO:
    def __init__(self):
        self.trafficFlow=None
        query_data = query_db()
        query = "SELECT * FROM `nus-competition.Traffic.traffic_flow`"
        self.traffic_flow_df = query_data.run_query(query)

    def convert_date(self, date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d/%m/%Y")

    def loadFromLocal(self):
        # with open("./sample_assets/trafficflow.json",mode='r') as f:
        #     jsonObject=json.load(f)

        # df=pd.DataFrame(jsonObject['Value'])
        df=self.traffic_flow_df
        df['Date'] = df['Date'].astype(str).apply(self.convert_date)
        
        df[['Volume','StartLat','StartLon']]=df[['Volume','StartLat','StartLon']].astype('float32')

        df2=df.filter(items=['LinkID','Volume']).groupby('LinkID').aggregate('max').reset_index('LinkID').rename(columns={'Volume':'maxVolume'})


        df3=pd.merge(df,df2,on='LinkID',how='left')
        df3['Congestion Levels']=(df3['Volume']/df3['maxVolume'])*10

        df3[['Congestion Levels']]=df3[['Congestion Levels']].astype('int')

        df3['size']=(df3['Congestion Levels']/20)

        #df3['Date']=df3['Date']+" "+df3['HourOfDate']+":00"
        df3['Date']=df3['Date']+" "+df3['HourOfDate'].astype(str)+":00"

        self.trafficFlow=df3
        #return(self.trafficFlow)

    def getScattermapbox(self,date):
        df=self.trafficFlow[(self.trafficFlow['Date']==date)]

        #scattermapbox=px.scatter_mapbox(df,lon='StartLon',lat='StartLat',color='Congestion Levels',size='size')
        scattermapbox = px.scatter_mapbox(df, lon='StartLon', lat='StartLat', color='Volume', size="Volume", opacity=0.5, size_max=15,
                                          color_continuous_scale=[(0, "grey"), (0.25, "grey"), 
                                                                  (0.25, "green"), (0.5, "green"), 
                                                                  (0.5, "orange"), (0.75, "orange"),
                                                                  (0.75, "red"), (1.00, "red")]
        )

        return(scattermapbox)
    
    def getDateList(self):
        return(self.trafficFlow.groupby('Date').aggregate('count').reset_index('Date')['Date'].to_list())

