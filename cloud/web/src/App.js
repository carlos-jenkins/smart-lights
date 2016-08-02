import React, { Component } from 'react';
import { GoogleMapLoader, GoogleMap, InfoWindow, Marker } from 'react-google-maps';
import { triggerEvent } from 'react-google-maps/lib/utils';

import api from './helpers/grid_api';
import './App.css';

class App extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {
            // Center Google Map in Costa Rica
            center: {
              lat: 10.0416216,
              lng: -84.1810092,
            },
            markers: []
          }
    }

    componentDidMount() {
        var self = this;
        api.getGrid(function(err, data) {
            self.setState({ markers: data});
        });
    }

    render() {
        console.log(this.state)
        return (
            <div className="container">
                <h1>Open Semaphore</h1>
                <GoogleMapLoader
                    containerElement={ <div className="row map-container"/> }
                    googleMapElement={
                        <GoogleMap
                            ref='map'
                            center={this.state.center}
                            defaultZoom={8}
                            defaultOptions={{
                                styles: require('./styledMap.json')
                            }}>
                            {this.state.markers.map((marker, index) => {
                                const ref = `marker_${index}`;
                                var latitude = marker.latitude;
                                var longitude = marker.longitude;

                                return (
                                    <Marker
                                        key={index}
                                        ref={ref}
                                        position={
                                            new google.maps.LatLng(latitude, longitude)
                                        }/>
                                );
                            })}
                        </GoogleMap>
                    }/>
            </div>
        );
    }
}

export default App;
