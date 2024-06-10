import React from 'react';
import {createRoot} from 'react-dom/client';
import { useState, useEffect, useRef } from "react"; 
import { GoogleMap } from '@react-google-maps/api';
import queryString from "query-string"
import Poly from './googlemaps';
import { useGoogleMap } from '@react-google-maps/api';
import fs from 'fs'

import {
    APIProvider,
    Map,
    useMapsLibrary,
    useMap
} from '@vis.gl/react-google-maps';
import { error } from 'console';

export default function App() {
  const mapRef = useRef(null);
  var tester=queryString.parse(window.location.search);
  
  const position = { lat: 43.6532, lng: -79.3832 };

  return (
      <div style={{ width: '100vw', height: '100vh' }}>
          <APIProvider apiKey={process.env.GOOGLE_MAPS_API_KEY}>
              <Map 
                  ref={mapRef}
                  gestureHandling={'greedy'}
                  fullscreenControl = {false}
                  mapId={process.env.GOOGLE_MAP_ID}           
              >
                <Directions />
                <MapLegend />
              </Map>
          </APIProvider> 
      </div>
  );
}

function Directions() {
  const [isMinimized, setIsMinimized] = useState(window.innerWidth < 768);
  const [isOpen, setIsOpen] = useState(true)
  
  const [selectedRouteIndex, setSelectedRouteIndex] = useState(0);
  const [polylines, setPolylines] = useState([]);
  const [polylinePath,setPolylinePath]=useState([]);
  const [departureTime, setDepartureTime] = useState(() => {
    const now = new Date();
    const utcOffset = now.getTimezoneOffset() * 60000; // Convert offset to milliseconds
    const sgTime = new Date(now.getTime() + utcOffset + (8 * 3600 * 1000)); // Convert to Singapore time
    return sgTime;
  });
  const [arrivalTime, setArrivalTime] = useState(null);


  var tester=queryString.parse(window.location.search);
  let origin, destination;

  const toggleOpen = () => {
    setIsOpen(!isOpen);
  };

  const toggleMinimize = () => {
    setIsMinimized(!isMinimized);
  };
  
  try {
    
    const points = tester.body ? JSON.parse(tester.body) : null;
    if (points && Array.isArray(points) && points.length >= 2) {
      origin = points[0];
      destination = points[1];
    } else {
      throw new Error("Invalid or missing origin and destination points in the 'body' parameter.");
    }
  } catch (error) {
    console.error("Failed to parse 'body' as JSON or invalid data format:", error);
    
    origin = "SMU, Singapore";
    destination = "NUS, Singapore";
  }

  const map = useMap();
  const routesLibrary = useMapsLibrary("routes")
  const [directionsService, setDirectionsService] =
    useState<google.maps.DirectionsService>();
  const [directionsRenderer, setDirectionsRenderer] = 
    useState<google.maps.DirectionsRenderer>();
  const [routes, setRoutes] = useState<google.maps.DirectionsRoute[]>([]);
  const [routeIndex, setRouteIndex] = useState(0);
  const selected = routes[routeIndex];
  
  const trafficLayerRef = useRef(null);
  

  useEffect(() => {
    if (!routesLibrary || !map) return;
    const ds = new routesLibrary.DirectionsService();
    const dr = new routesLibrary.DirectionsRenderer({
      map: map,
      polylineOptions: {
        strokeColor: '#0000FF',
        strokeOpacity: 0.8,
        strokeWeight: 6
      }
    });

    setDirectionsService(ds);
    setDirectionsRenderer(dr);

    const trafficLayer = new google.maps.TrafficLayer();
    trafficLayer.setMap(map);
    trafficLayerRef.current = trafficLayer;
  }, [routesLibrary, map]);

  useEffect(() => {
    if (trafficLayerRef.current) {
      trafficLayerRef.current.setMap(map);
    }
  }, [map]);

  useEffect(() => {
    if(!directionsService || !directionsRenderer || !departureTime) return;

    directionsService.route({
      origin: origin,
      destination: destination,
      travelMode: google.maps.TravelMode.DRIVING,
      drivingOptions: {
        departureTime: departureTime,
        trafficModel: 'pessimistic'
      },
      provideRouteAlternatives: true,
    })
    .then(response => {
      directionsRenderer.setDirections(response);
      setRoutes(response.routes);
      if (response.routes.length > 0) {
        const durationInSeconds = response.routes[0].legs[0].duration.value;
        const estimatedArrival = new Date(departureTime.getTime() + durationInSeconds * 1000);
        setArrivalTime(estimatedArrival);
    }
});
}, [directionsService, directionsRenderer, departureTime]);
  

  

  useEffect(() => {
    if (routes.length > 0 && routes[selectedRouteIndex]) {
      const durationInSeconds = routes[selectedRouteIndex].legs[0].duration.value;
      const estimatedArrival = new Date(departureTime.getTime() + durationInSeconds * 1000);
      setArrivalTime(estimatedArrival);
    }
  }, [selectedRouteIndex, routes, departureTime]);
  
  const handleRouteChange = (index) => {
    setSelectedRouteIndex(index);
    // Calculate new estimated arrival time
    const selectedRoute = routes[index];
    const durationInSeconds = selectedRoute.legs[0].duration.value;
    const estimatedArrival = new Date(departureTime.getTime() + durationInSeconds * 1000);
    setArrivalTime(estimatedArrival);
  };

  useEffect(() => {
    if (directionsRenderer) {
      directionsRenderer.setRouteIndex(selectedRouteIndex);
    }
  }, [selectedRouteIndex, directionsRenderer, routes]);
  
  //var speedBandResponse=fetch('http://fuqianshan.asuscomm.com:5173/speedBand.json')
  //var speedBandData=speedBandResponse.json()

  /*const polylinePath = [
    {path:[
      //{ lat: speedBandData.value[0].StartLat, lng: speedBandData.value[0].StartLon },
      //{ lat: speedBandData.value[0].EndLat, lng: speedBandData.value[0].EndLon },
      { lat: 1.350438529, lng: 103.6944089 },
      { lat: 1.29779483, lng: 103.8986301 },
    ], color: '#FF0000'},
    {path:[
      //{ lat: speedBandData.value[1].StartLat, lng: speedBandData.value[1].StartLon },
      //{ lat: speedBandData.value[1].EndLat, lng: speedBandData.value[1].EndLon },
      {lat: 1.29779483, lng: 103.8986301},
      { lat: 1.374880256, lng: 103.9344163 },
    ], color: '#0000FF'} 
  ];*/
  const toSingaporeTimeString = (date) => {
    // Format date as local time, slicing to fit 'datetime-local' input without seconds
    return new Date(date.getTime() - (date.getTimezoneOffset() * 60000))
      .toISOString()
      .slice(0, 16);
  };


  
  const handleDateChange = (event) => {  
    const localDate = new Date(event.target.value);
    const utcDate = new Date(localDate.getTime() + (localDate.getTimezoneOffset() * 60000));
    const sgDate = new Date(utcDate.getTime() + 8 * 3600 * 1000);
    setDepartureTime(sgDate);
  };

  const displayArrivalTime = () => {
    return arrivalTime ? arrivalTime.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: 'numeric',
        hour12: true
    }) : 'Calculating...';
};
  
  const selectedRoute = routes[selectedRouteIndex];
  const leg = selectedRoute ? selectedRoute.legs[0] : null;

  if (!leg) return null;

  if (!isOpen) return null;
  
  return (
    <div className="directions" style={{
      padding: '10px',
      boxShadow: '0 2px 6px rgba(0,0,0,0.1)',
      backgroundColor: 'white',
      borderRadius: '8px',
      margin: '20px',
      maxWidth: '90vw',
      boxSizing: 'border-box',
      position: 'absolute',
      zIndex: 1001
    }}>
      <button onClick={toggleMinimize} style={{ fontSize: '1rem' }}>
        {isMinimized ? 'Expand Legend' : 'Minimize'}
      </button>
      {!isMinimized && (
        <>
          <h2 style={{ fontSize: '1.2rem' }}>
            {routes[selectedRouteIndex]?.summary}
          </h2>
          <p>
          {leg.start_address.split(",")[0]} to {leg.end_address.split(",")[0]}
          </p>
          <p>Distance: {leg.distance?.text}</p>
          <p>Estimated Arrival Time: {displayArrivalTime()}</p>

          <div style={{ margin: '10px 0' }}>
            <label>Departure Time: </label>
            <input
              type="datetime-local"
              value={toSingaporeTimeString(departureTime)}
              onChange={handleDateChange}
            />
          </div>
  
          <h2 style={{ fontSize: '1rem' }}>Other Routes</h2>
          <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
            {routes.map((route, index) => (
              <li key={route.summary}>
                <button onClick={() => handleRouteChange(index)} style={{
                  backgroundColor: '#007BFF',
                  color: 'white',
                  border: 'none',
                  borderRadius: '5px',
                  padding: '10px 15px',
                  margin: '5px',
                  fontSize: '1rem',
                  width: '100%',
                  textAlign: 'left'
                }}>
                  {route.summary}
                </button>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );  
}

const Markers = () => {
  return null
}

function MapLegend() {
  return (
    <div style={{
      position: 'absolute', 
      bottom: '20px',
      right: '20px',
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      padding: '10px',
      borderRadius: '5px',
      zIndex: 1000 
    }}>
      <h4>Traffic Conditions</h4>
      <div><span style={{ display: 'inline-block', width: '20px', height: '10px', backgroundColor: '#28a745' }}></span> Smooth Traffic</div>
        <div><span style={{ display: 'inline-block', width: '20px', height: '10px', backgroundColor: '#ffc107' }}></span> Slow moving</div>
        <div><span style={{ display: 'inline-block', width: '20px', height: '10px', backgroundColor: '#dc3545' }}></span> Traffic jams</div>
    </div>
  );
}


export function renderToDom(container: HTMLElement) {
  const root = createRoot(container);

  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
}