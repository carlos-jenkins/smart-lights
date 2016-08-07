import React, { Component } from 'react';
import moment from 'moment';
import rd3 from 'rd3';
import _ from 'underscore';

import api from './helpers/api';
import './Dashboard.css';

const LineChart = rd3.LineChart;
var self;

class Dashboard extends Component {
    constructor(props, context) {
        super(props, context);
        self = this;
        this.state = {
            data: [{
                audio: '0',
                humidity: '0.0',
                timestamp: '',
                pressure: '0.0',
                state: '',
                gas: '0',
                id_semaphore: '',
                temperature: '0.0'
            }],
            showAudio: false,
            showTemperature: false,
            showHumidity: false,
            showPressure: false
        }
    }

    componentDidMount() {
        this._timer = setInterval(this._tick, 1000);
    }

    componentWillUnmount() {
        clearInterval(this._timer);
    }

    render() {
        var semaphore = _.last(this.state.data);
        var audio = parseInt(semaphore.audio);
        var temperature = parseFloat(semaphore.temperature);
        var humidity = parseFloat(semaphore.humidity);
        var pressure = parseFloat(semaphore.pressure);

        return (
            <div className="container">
                <div className="row">
                    <div className="col s12">
                        <h1>Dashboard</h1>
                    </div>

                </div>

                <div className="sensor-wrapper">
                    <div className="row">
                        <div className="col s3">
                            <h2>State</h2>
                        </div>
                        <div className="col s3">
                            <div className="trafficlight">
                                <div className={`red ${this.state.active === 'red' ? '' : 'inactive'}`} onClick={() => { this._toggleRed() }}/>
                                <div className={`yellow ${this.state.active === 'yellow' ? '' : 'inactive'}`} onClick={() => { this._toggleYellow() }}/>
                                <div className={`green ${this.state.active === 'green' ? '' : 'inactive'}`} onClick={() => { this._toggleGreen() }}/>
                            </div>
                        </div>
                        <div className="col s6">
                            <h5>{moment().format('MMMM Do YYYY, h:mm:ss a')}</h5>
                        </div>
                    </div>
                </div>

                {/* Noise */ }
                <div className="sensor-wrapper" onClick={() => { this.setState({showAudio: !this.state.showAudio}) }}>
                    <div className="row">
                        <div className="col s6">
                            <h2>Noise <i className="material-icons expand-more"><h2>{this.state.showAudio ? 'expand_less' : 'expand_more'}</h2></i></h2>
                        </div>
                        <div className="col s6">
                            <div className="circle-outer">
                                <div className="circle-inner">
                                    {Math.floor(audio/10)}<strong>dB</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                    {this.state.showAudio && <div className="row">
                        <div className="col s12">
                            <LineChart
                                legend={true}
                                data={[{
                                        name: 'audio',
                                        values: _.chain(this.state.data).pluck('audio')
                                                .map(function(a, i) { return {
                                                    x: i, y: parseInt(a, 10)
                                                }}).value(),
                                        strokeWidth: 3,
                                        strokeDashArray: '5,5',
                                }]}
                                width='100%'
                                height={400}
                                viewBoxObject={{
                                  x: 0,
                                  y: 0,
                                  width: 1000,
                                  height: 400
                                }}
                                domain={{x: [,6], y: [-10,]}}
                                gridHorizontal={true}
                              />
                        </div>
                    </div>}
                </div>
                {/* Temperature */ }
                <div className="sensor-wrapper" onClick={() => { this.setState({showTemperature: !this.state.showTemperature}) }}>
                    <div className="row">
                        <div className="col s6">
                            <h2>Temperature <i className="material-icons expand-more"><h2>{this.state.showTemperature ? 'expand_less' : 'expand_more'}</h2></i></h2>
                        </div>
                        <div className="col s6">
                            <div className="circle-outer thermometer-outer">
                                <div className="circle-inner">
                                    {Math.floor(temperature)}<span>{`.${Math.round((temperature.toFixed(1) % 1) * 10)}`}</span><strong>&deg;</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                    {this.state.showTemperature && <div className="row">
                        <div className="col s12">
                            <LineChart
                                legend={true}
                                data={[{
                                        name: 'temperature',
                                        values: _.chain(this.state.data).pluck('temperature')
                                                .map(function(a, i) { return {
                                                    x: i, y: parseInt(a, 10)
                                                }}).value(),
                                        strokeWidth: 3,
                                        strokeDashArray: '5,5',
                                }]}
                                width='100%'
                                height={400}
                                viewBoxObject={{
                                  x: 0,
                                  y: 0,
                                  width: 1000,
                                  height: 400
                                }}
                                domain={{x: [,6], y: [-10,]}}
                                gridHorizontal={true}
                              />
                        </div>
                    </div>}
                </div>
                {/* Humidity */ }
                <div className="sensor-wrapper" onClick={() => { this.setState({showHumidity: !this.state.showHumidity}) }}>
                    <div className="row">
                        <div className="col s6">
                            <h2>Humidity <i className="material-icons expand-more"><h2>{this.state.showHumidity ? 'expand_less' : 'expand_more'}</h2></i></h2>
                        </div>
                        <div className="col s6">
                            <div className="circle-outer">
                                <div className="circle-inner">
                                    {Math.floor(humidity)}<span>{`.${Math.round((humidity.toFixed(1) % 1) * 10)}`}</span><strong>%</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                    {this.state.showHumidity && <div className="row">
                        <div className="col s12">
                            <LineChart
                                legend={true}
                                data={[{
                                        name: 'humidity',
                                        values: _.chain(this.state.data).pluck('humidity')
                                                .map(function(a, i) { return {
                                                    x: i, y: parseInt(a, 10)
                                                }}).value(),
                                        strokeWidth: 3,
                                        strokeDashArray: '5,5',
                                }]}
                                width='100%'
                                height={400}
                                viewBoxObject={{
                                  x: 0,
                                  y: 0,
                                  width: 1000,
                                  height: 400
                                }}
                                domain={{x: [,6], y: [-10,]}}
                                gridHorizontal={true}
                              />
                        </div>
                    </div>}
                </div>
                {/* Pressure */ }
                <div className="sensor-wrapper" onClick={() => { this.setState({showPressure: !this.state.showPressure}) }}>
                    <div className="row">
                        <div className="col s6">
                            <h2>Pressure <i className="material-icons expand-more"><h2>{this.state.showPressure ? 'expand_less' : 'expand_more'}</h2></i></h2>
                        </div>
                        <div className="col s6">
                            <div className="circle-outer">
                                <div className="circle-inner">
                                    {Math.floor(pressure)}<span>{`.${Math.round((pressure.toFixed(1) % 1) * 10)}`}</span><strong>hPa</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                    {this.state.showPressure && <div className="row">
                        <div className="col s12">
                            <LineChart
                                legend={true}
                                data={[{
                                        name: 'pressure',
                                        values: _.chain(this.state.data).pluck('pressure')
                                                .map(function(a, i) { return {
                                                    x: i, y: parseInt(a, 10)
                                                }}).value(),
                                        strokeWidth: 3,
                                        strokeDashArray: '5,5',
                                }]}
                                width='100%'
                                height={400}
                                viewBoxObject={{
                                  x: 0,
                                  y: 0,
                                  width: 1000,
                                  height: 400
                                }}
                                domain={{x: [,6], y: [-10,]}}
                                gridHorizontal={true}
                              />
                        </div>
                    </div>}
                </div>
            </div>
        );
    }

    _tick() {
        api.getLastQty({ qty: 10 }, function(tail) {
            self.setState({ data: tail });
        })
    }

    _toggleGreen() {
        this.setState({ active: 'green' });
    }

    _toggleRed() {
        this.setState({ active: 'red' });
    }

    _toggleYellow() {
        this.setState({ active: 'yellow' });
    }
}

export default Dashboard;
