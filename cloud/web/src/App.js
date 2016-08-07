import React, { Component } from 'react';
import { GoogleMapLoader, GoogleMap, Marker } from 'react-google-maps';
import { triggerEvent } from "react-google-maps/lib/utils";
import { Link } from 'react-router'

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
            markers: [{
                id: 2,
                latitude: 9.9454167,
                longitude: -84.1491331,
                name: 'Multiplaza del Este'
            },
            {
                id: 1,
                latitude: 9.9412773,
                longitude: -84.082515,
                name: 'Museo de los Niños'
            }],
            containerMapClass: 'col s12 map-container'
          }
    }

    render() {
        return (
            <div className="container">
                <h1>Open Semaphore</h1>
                <div className="row row-wrapper">
                    <GoogleMapLoader
                        containerElement={ <div className={this.state.containerMapClass}/> }
                        googleMapElement={
                            <GoogleMap
                                ref='_map'
                                center={this.state.center}
                                defaultZoom={8}
                                defaultOptions={{
                                    styles: require('./styledMap.json')
                                }}
                                onClick={() => { this._onMapClick() }}>
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
                                            }
                                            onClick={() => { this._onMarkerClick(marker) }}/>
                                    );
                                })}
                            </GoogleMap>
                    }/>
                    <div className="col s5">
                        {this.state.selectedMarker && <div>
                            <h3>{this.state.selectedMarker.name}</h3>
                            <p><strong>Latitude: </strong>{this.state.selectedMarker.latitude}</p>
                            <p><strong>Longitude: </strong>{this.state.selectedMarker.longitude}</p>
                            <Link className='btn'
                                to={`/dashboard/${this.state.selectedMarker.id}`}>
                                Show Dashboard
                            </Link>
                        </div>}
                    </div>
                </div>
            </div>
        );
    }

    _onMarkerClick(marker) {
        var isSameMarker =  this.state.selectedMarker === marker;
        var containerMapClass = (isSameMarker || this.state.selectedMarker) ?
                                'col s12 map-container' : 'col s7 map-container';
        this.setState({
            selectedMarker: isSameMarker ? null : marker,
            containerMapClass: containerMapClass
        })
        // triggerEvent(this._map, 'resize');
    }

    _onMapClick() {
        this.setState({
            selectedMarker: null,
            containerMapClass: 'col s12 map-container'
        })
        // triggerEvent(this._map, 'resize');
    }
}

export default App;
