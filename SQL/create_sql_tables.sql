create schema competition;
use competition;


create table traffic_incidents (
	Type varchar(255) not null,
    Latitude double not null,
    Longitude double not null,
	Message varchar(255) not null primary key,
    Date_time varchar(255) not null
);

create table faulty_traffic_lights (
	AlarmID varchar(255) not null,
    NodeID varchar(255) not null,
    Type int,
    StartDate datetime,
    EndDate datetime,
    Message varchar(255),
    constraint faulty_traffic_lights_pk primary key (AlarmID, NodeID)
);

create table road_openings (
	EventID varchar(255) not null primary key,
    StartDate datetime,
    EndDate datetime,
    SvcDept varchar(255),
    RoadName varchar(255),
    Other varchar(255)
);

create table road_works (
	EventID varchar(255) not null primary key,
    StartDate datetime,
    EndDate datetime,
    SvcDept varchar(255),
    RoadName varchar(255),
    Other varchar(255)
);

create table estimated_travel_times (
	Name varchar(55) not null,
    Direction int,
    FarEndPoint varchar(55),
    StartPoint varchar(55),
    EndPoint varchar(55),
    EstTime int,
    constraint estimated_travel_times_pk primary key (Name, Direction, FarEndPoint, StartPoint, EndPoint, EstTime)
);

create table carpark_avail (
	CarParkID varchar(55) not null primary key,
    Area varchar(255),
    Development varchar(255),
    Location varchar(255),
    AvailableLots int,
    LotType char(1),
    Agency varchar(3)
);


CREATE TABLE bus_routes (
    ServiceNo int,
    Operator varchar(255),
    Direction int,
    StopSequence int,
    BusStopCode int,
    Distance real,
    WD_FirstBus varchar(255),
    WD_LastBus varchar(255),
    SAT_FirstBus varchar(255),
    SAT_LastBus varchar(255),
    SUN_FirstBus varchar(255),
    SUN_LastBus varchar(255)
);

CREATE TABLE bus_stops (
    BusStopCode varchar(255),
    RoadName varchar(255),
    Description varchar(255),
    Latitude real,
    Longitude real
);

CREATE TABLE taxi_availability (
    Longitude real,
    Latitude real
);

CREATE TABLE taxi_stands (
    TaxiCode varchar(255),
    Latitude real,
    Longitude real,
    Bfa varchar(255),
    Ownership varchar(255),
    Type varchar(255),
    Name varchar(255)
);

CREATE TABLE erp_rates (
    VehicleType varchar(255),
    DayType varchar(255),
    StartTime datetime,
    EndTime datetime,
    ZoneID varchar(255),
    ChargeAmount real,
    EffectiveDate varchar(255)
);

CREATE TABLE traffic_speed_bands (
    LinkID varchar(255),
    RoadName varchar(255),
    RoadCategory varchar(255),
    SpeedBand int,
    MinimumSpeed varchar(255),
    MaximumSpeed varchar(255),
    StartLon real,
    StartLat real,
    EndLon real,
    EndLat real
);

CREATE TABLE traffic_flow (
    LinkID varchar(255),
    Date varchar(255),
    HourOfDate varchar(255),
    Volume varchar(255),
    StartLon real,
    StartLat real,
    EndLon real,
    EndLat real,
    RoadName varchar(255),
    RoadCat varchar(255)
);
