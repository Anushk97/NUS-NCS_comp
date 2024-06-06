import React, { useEffect, useRef } from 'react';
import queryString from 'query-string';
import { GoogleMap, useJsApiLoader, Polyline } from '@react-google-maps/api';

const containerStyle = {
  width: '100vw',
  height: '100vh'
};

const center = { lat:  1.350438529, lng: 103.6944089 };

function Poly() {
    const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: process.env.GOOGLE_MAPS_API_KEY
});

  const mapRef = useRef(null);
  const queryParams = queryString.parse(window.location.search);

  let origin = queryParams.origin ? JSON.parse(queryParams.origin) : center;
  let destination = queryParams.destination ? JSON.parse(queryParams.destination) : { lat: 1.350438529, lng: 103.6944089 };

  const path = [
    origin,
    destination,
    { lat: 1.350438529, lng: 103.6944089 }, 
    { lat: 1.29779483, lng: 103.8986301 }
  ];

  return (
    <div style={containerStyle}>
      {isLoaded && (
        <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={12}
        onLoad={map => mapRef.current = map}
        mapTypeControl={false}
    >
        <Polyline
        path={path}
        options={{
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#FF0000',
            fillOpacity: 0.35,
            clickable: false,
            draggable: false,
            editable: false,
            visible: true,
            radius: 30000,
            zIndex: 1
            }}
        />
        </GoogleMap>
    )}
    </div>
);
}

export default Poly;
