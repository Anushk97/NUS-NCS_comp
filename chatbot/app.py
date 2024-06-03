import gradio as gr
import pandas as pd
import plotly.graph_objects as go
from FacilitiesMaintenanceDAO import FacilitiesMaintenanceDAO
from VolumeByBusStopDAO import VolumeByBusStopDAO
from VolumeByTrainStationDAO import VolumeByTrainStationDAO
from RoadWorksDAO import RoadWorksDAO
from TrafficFlowDAO import TrafficFlowDAO
from sustainability import sustainability
from LLMOpenAIInterface import docRetriever, LLMOpenAI
from LLMSQLInterface import LLMSQLInterface
from bigq_extract import query_db

# Extract data from BigQuery
query_data = query_db()

## Tab 1
showContent=[]
hideContent=[]
for i in range(6):
    showContent.append(None)
    hideContent.append(None)
guideText=''.join(open("./sample_assets/guideText.txt",mode="r").readlines())


## chart 0: traffic incidents barplot
def currentFunction():
    return(gr.Group(visible=True),gr.Column(visible=False),gr.Button(visible=True))
showContent[0]=currentFunction

def currentFunction():
    return(gr.Group(visible=False),gr.Column(visible=True),gr.Button(visible=False))
hideContent[0]=currentFunction

query = "SELECT * FROM `nus-competition.Traffic.traffic_incidents`"
traffic_incidents_df = query_data.run_query(query)

trafficIncidents=traffic_incidents_df.groupby("Type").size().reset_index(name='counts')


## chart 1: road works
roadWorksDAO=RoadWorksDAO()
roadWorksDAO.loadLocalData()

def currentFunction():
    return(gr.Group(visible=True),gr.Column(visible=False),gr.Button(visible=True))
showContent[1]=currentFunction

def currentFunction():
    return(gr.Group(visible=False),gr.Column(visible=True),gr.Button(visible=False))
hideContent[1]=currentFunction

def filterByRoadName(selectedRoadName):
    return(
        gr.Dataframe(
            value=roadWorksDAO.getDataframeByRoadName(selectedRoadName),
            show_label=False,
            wrap=True
        ))

## chart 2: Facilities Maintenance
facilitiesMaintenanceDAO=FacilitiesMaintenanceDAO()
facilitiesMaintenanceDAO.loadFromCSV()

def currentFunction():
    return(gr.Group(visible=True),gr.Column(visible=False),gr.Button(visible=True))
showContent[2]=currentFunction

def currentFunction():
    return(gr.Group(visible=False),gr.Column(visible=True),gr.Button(visible=False))
hideContent[2]=currentFunction

def filterByStationName(selectedStationName):
    return(
        gr.Dataframe(
            value=facilitiesMaintenanceDAO.getDataframeByStationName(selectedStationName),
            show_label=False,
            wrap=True
        ))


## chart 3: Passenger volume by Bus Stop
def currentFunction():
    return(gr.Group(visible=True),gr.Column(visible=False),gr.Button(visible=True))
showContent[3]=currentFunction

def currentFunction():
    return(gr.Group(visible=False),gr.Column(visible=True),gr.Button(visible=False))
hideContent[3]=currentFunction

volumeByBusStopDAO=VolumeByBusStopDAO()
volumeByBusStopDAO.loadLocalData()


## chart 4: Passenger volume by Train Station
def currentFunction():
    return(gr.Group(visible=True),gr.Column(visible=False),gr.Button(visible=True))
showContent[4]=currentFunction

def currentFunction():
    return(gr.Group(visible=False),gr.Column(visible=True),gr.Button(visible=False))
hideContent[4]=currentFunction

volumeByTrainStationDAO=VolumeByTrainStationDAO()
volumeByTrainStationDAO.loadLocalData()


## Tab 2

trafficFlowDAO=TrafficFlowDAO()
trafficFlowDAO.loadFromLocal()
#densitymapbox=trafficFlowDAO.getScattermapbox('01/11/2023')

def filter_map(date='01/11/2023 7:00'):
    if date=="__Most Recent__":
        thisDate='01/11/2023 7:00'
    else:
        thisDate=date
    densitymapbox=trafficFlowDAO.getScattermapbox(thisDate)
    fig = go.Figure(densitymapbox)

    fig.update_layout(
        autosize=True,
        mapbox_style="open-street-map",
        hovermode='closest',
        mapbox=dict(
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=1.368,
                lon=103.794
            ),
            pitch=0,
            zoom=10
        ),
    )

    return fig



# GUI 

db_llm = LLMSQLInterface()
doc_llm = LLMOpenAI()
sustainability_forecast = sustainability()

try:
    demo.close()
except:
    pass

with gr.Blocks(title="BooleanPirates") as demo:
    with gr.Row(variant='panel'):
        with gr.Column():
            gr.Tab("TransportGPT",interactive=False)
            with gr.Column():          
                with gr.Tab("Query Database"):
                    with gr.Group():
                        chatbot=gr.Chatbot(show_label=True)
                        msg=gr.Textbox(placeholder="Press enter to submit your query")
                        clear=gr.ClearButton([msg,chatbot],value="Clear")
                        msg.submit(db_llm.create_conversation,[msg,chatbot],[msg,chatbot])

                with gr.Tab("Query Document"):
                    with gr.Column("Document Upload", elem_classes=["upload_container"]):
                        gr.Interface(
                            fn=doc_llm.process_file,
                            inputs=["file"],
                            outputs="text",
                            title="File Uploader",
                            description="Upload a file to start document search (Supported file types: DOCX, TXT, PDF, CSV)",
                            allow_flagging="auto"
                        )
                    with gr.Column("Chatbot 2", elem_classes=["chatbot2_container"]):
                        chatbot = gr.Chatbot(show_label=True)
                        msg=gr.Textbox(placeholder="Press enter to submit your query")
                        clear = gr.ClearButton([msg, chatbot])
                        msg.submit(doc_llm.create_conversation, [msg, chatbot], [msg, chatbot])
            
        with gr.Column(min_width=950):
            gr.Tab("TransportViz",interactive=False)
            with gr.Column():
                with gr.Tab("Charts"):
                    with gr.Column() as dashboard:
                        with gr.Column() as dashboardSelector:
                            with gr.Row():
                                buttons=[
                                    gr.Button(
                                        value="Traffic Incidents",
                                        scale=4,
                                        #icon="./sample_assets/testImage.png"
                                        ),
                                    gr.Button(
                                        value="Road Works",
                                        scale=4,
                                        #icon="./sample_assets/testImage.png"
                                        ),
                                    gr.Button(
                                        value="Train Station Facility Maintenance",
                                        scale=4,
                                        #icon="./sample_assets/testImage.png"
                                        ),
                                    gr.Button(
                                        value="Bus Stop Passenger Volume",
                                        scale=4,
                                        #icon="./sample_assets/testImage.png"
                                        ),
                                    gr.Button(
                                        value="Train Station Passenger Volume",
                                        scale=4,
                                        #icon="./sample_assets/testImage.png"
                                        )
                                ]
                            defaultGuide=gr.Textbox(value=guideText,label="")

                        with gr.Group() as container:
                            returnButtons=[
                                gr.Button(value="Back",visible=False),
                                gr.Button(value="Back",visible=False),
                                gr.Button(value="Back",visible=False),
                                gr.Button(value="Back",visible=False),
                                gr.Button(value="Back",visible=False)
                            ]
                            contents=[
                                gr.Group(
                                    visible=False
                                    ),
                                gr.Group(
                                    visible=False,
                                    ),
                                gr.Group(
                                    visible=False,
                                    ),
                                gr.Group(
                                    visible=False,
                                    ),
                                gr.Group(
                                    visible=False,
                                    )
                            ]
                            with contents[0]:
                                gr.Label(value="Traffic Incidents",show_label=False)
                                gr.BarPlot(
                                    show_label=False,
                                    value=trafficIncidents,
                                    x="Type",
                                    y="counts",
                                    vertical=False,
                                    tooltip=["counts"],
                                    height=360,
                                    width=720,
                                    color="Type"
                                )

                            with contents[1]:
                                gr.Label(value="Road Works",show_label=False)
                                gr.Label(value="Currently there's "+str(roadWorksDAO.roadWorks.shape[0])+" road work items existing",show_label=False)
                                roadWorksDropDown=gr.Dropdown(["__ALL__"]+roadWorksDAO.getUniqueRoadNameList(),label="Type here then select to filter by road name")
                                roadWorksDataframe=gr.Dataframe(
                                    value=roadWorksDAO.roadWorks,
                                    show_label=False,
                                    wrap=True
                                )

                            roadWorksDropDown.change(filterByRoadName,roadWorksDropDown,roadWorksDataframe)

                            with contents[2]:
                                gr.Label(value="Train Station Facility Maintenance",show_label=False)
                                gr.Label(value="There's "+str(len(facilitiesMaintenanceDAO.getUniqueStationNameList()))+" stations with maintenance item",show_label=False)
                                facilitiesMaintenanceDropDown=gr.Dropdown(["__ALL__"]+facilitiesMaintenanceDAO.getUniqueStationNameList(),label="Type here then select to filter by station name")
                                facilitiesMaintenanceDataframe=gr.Dataframe(
                                    value=facilitiesMaintenanceDAO.pdTable,
                                    show_label=False,
                                    wrap=True
                                )
                            
                            facilitiesMaintenanceDropDown.change(filterByStationName,facilitiesMaintenanceDropDown,facilitiesMaintenanceDataframe)

                            with contents[3]:
                                gr.Label(value="Bus Stop Passenger Volume",show_label=False)
                                with gr.Row():
                                    chart3_1=gr.BarPlot(
                                        label="Boarding",
                                        value=volumeByBusStopDAO.volumeByBusStop.sort_values(by="TOTAL_TAP_IN_VOLUME",ascending=False).head(10),
                                        x="Description",
                                        x_title="Bus Stop",
                                        x_label_angle=45,
                                        y="TOTAL_TAP_IN_VOLUME",
                                        y_title="Boarding Volume",
                                        tooltip=["PT_CODE","RoadName","Description","TOTAL_TAP_IN_VOLUME"],
                                        height=360,
                                        width=475
                                        )
                                    chart3_2=gr.BarPlot(
                                        label="Alighting",
                                        value=volumeByBusStopDAO.volumeByBusStop.sort_values(by="TOTAL_TAP_OUT_VOLUME",ascending=False).head(10),
                                        x="Description",
                                        x_title="Bus Stop",
                                        x_label_angle=45,
                                        y="TOTAL_TAP_OUT_VOLUME",
                                        y_title="Alighting Volume",
                                        tooltip=["PT_CODE","RoadName","Description","TOTAL_TAP_OUT_VOLUME"],
                                        height=360,
                                        width=475
                                        )
                            
                            with contents[4]:
                                gr.Label(value="Train Station Passenger Volume",show_label=False)
                                with gr.Row():
                                    chart4_1=gr.BarPlot(
                                        label="Boarding",
                                        value=volumeByTrainStationDAO.volumeByTrainStation.sort_values(by="TOTAL_TAP_IN_VOLUME",ascending=False).head(10),
                                        x="mrt_station_english",
                                        x_title="Train Station",
                                        x_label_angle=45,
                                        y="TOTAL_TAP_IN_VOLUME",
                                        y_title="Boarding Volume",
                                        tooltip=["PT_CODE","mrt_station_english","mrt_line_english","TOTAL_TAP_IN_VOLUME"],
                                        height=360,
                                        width=475
                                        )
                                    chart4_2=gr.BarPlot(
                                        label="Alighting",
                                        value=volumeByTrainStationDAO.volumeByTrainStation.sort_values(by="TOTAL_TAP_OUT_VOLUME",ascending=False).head(10),
                                        x="mrt_station_english",
                                        x_title="Train Station",
                                        x_label_angle=45,
                                        y="TOTAL_TAP_OUT_VOLUME",
                                        y_title="Alighting Volume",
                                        tooltip=["PT_CODE","mrt_station_english","mrt_line_english","TOTAL_TAP_OUT_VOLUME"],
                                        height=360,
                                        width=475
                                        )
                                                            
                        for i in range(5):
                            buttons[i].click(fn=showContent[i],outputs=[contents[i],dashboardSelector,returnButtons[i]])
                            returnButtons[i].click(fn=hideContent[i],outputs=[contents[i],dashboardSelector,returnButtons[i]])

                with gr.Tab("Traffic Flow Map"):
                    with gr.Group():
                        gr.Label(value="Traffic Flow Conditions",show_label=False)
                        trafficFlowDropdown=gr.Dropdown(["__Most Current__"]+trafficFlowDAO.getDateList(),value="01/01/2024 7:00",label="Select filter to get data by date&time")
                        map=gr.Plot(show_label=False)
                demo.load(filter_map,outputs=map)
                trafficFlowDropdown.change(filter_map,inputs=trafficFlowDropdown,outputs=map)

                with gr.Tab("Incident Response"):
                    gr.Markdown("### Welcome to the Incident Response Tool")
                    gr.Markdown("[Access here](http://fuqianshan.asuscomm.com:7920/)")
                    
                with gr.Tab("Sustainability Monitoring"):
                    with gr.Group():
                        final_year = gr.Radio([2025, 2026, 2027, 2028, 2029, 2030], label="Forecast to:")
                        show_legend = gr.Checkbox(label="Show Legend")
                        submit = gr.Button("Submit")
                        output_plot = gr.Plot(show_label=False)
                        submit.click(sustainability_forecast.plot_dataframes, [final_year, show_legend], output_plot)

demo.launch()