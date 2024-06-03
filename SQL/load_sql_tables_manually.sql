use competition;

LOAD DATA LOCAL INFILE './SQL/Data/bus_routes/bus_routes.csv'
INTO TABLE bus_routes
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './SQL/Data/bus_stops/bus_stops.csv'
INTO TABLE bus_stops
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './SQL/Data/carpark_avail/carpark_avail.csv'
INTO TABLE carpark_avail
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './SQL/Data/estimated_travel_times/estimated_travel_times.csv'
INTO TABLE estimated_travel_times
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './SQL/Data/faulty_traffic_lights/faulty_traffic_lights.csv'
INTO TABLE faulty_traffic_lights
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './SQL/Data/road_openings/road_openings.csv'
INTO TABLE road_openings
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './SQL/Data/road_works/road_works.csv'
INTO TABLE road_works
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './SQL/Data/taxi_availability/taxi_availability.csv'
INTO TABLE taxi_availability
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './SQL/Data/taxi_stands/taxi_stands.csv'
INTO TABLE taxi_stands
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './SQL/Data/traffic_flow/traffic_flow.csv'
INTO TABLE traffic_flow
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './SQL/Data/traffic_incidents/traffic_incidents.csv'
INTO TABLE traffic_incidents
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './SQL/Data/traffic_speed_bands/traffic_speed_bands.csv'
INTO TABLE traffic_speed_bands
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;










