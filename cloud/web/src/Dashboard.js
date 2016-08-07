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
                humidity: '',
                timestamp: '',
                pressure: '',
                state: '',
                gas: '',
                id_semaphore: '',
                temperature: ''
            }]
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
        return (
            <div className="container">
                <div className="row">
                    <div className="col s6">
                        <h1>Dashboard</h1>
                    </div>
                    <div className="col s6">
                        <h5>{moment().format('MMMM Do YYYY, h:mm:ss a')}</h5>
                    </div>
                </div>

                <div className="row">
                    <div className="col s3">
                        <h2>State</h2>
                    </div>
                    <div className="col s1">
                        <div className={`row ${this.state.active === 'red' ? 'red' : 'grey'} darken-1 circle`}
                            onClick={() => { this._toggleRed() }}/>
                        <div className={`row ${this.state.active === 'yellow' ? 'yellow' : 'grey'} darken-1 circle`}
                            onClick={() => { this._toggleYellow() }}/>
                        <div className={`row ${this.state.active === 'green' ? 'green' : 'grey'} darken-1 circle`}
                            onClick={() => { this._toggleGreen() }}/>
                    </div>
                </div>

                {/* Noise */ }
                <div className="row">
                    <div className="col s9">
                        <h2>Noise</h2>
                    </div>
                    <div className="col s3">
                        <h5>{`${semaphore.audio} dB`}</h5>
                    </div>
                </div>
                <div className="row">
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

                </div>
                {/* Temperature */ }
                <div className="row">
                    <div className="col s12">
                        <h2>Temperature</h2>
                    </div>
                </div>
                <div className="row">
                    <div className="col s6">
                        graphic here
                    </div>
                    <div className="col s6">
                        {semaphore.temperature}
                    </div>
                </div>
                {/* Humidity */ }
                <div className="row">
                    <div className="col s12">
                        <h2>Humidity</h2>
                    </div>
                </div>
                <div className="row">
                    <div className="col s6">
                        graphic here
                    </div>
                    <div className="col s6">
                        {semaphore.humidity}
                    </div>
                </div>
                {/* Pressure */ }
                <div className="row">
                    <div className="col s12">
                        <h2>Pressure</h2>
                    </div>
                </div>
                <div className="row">
                    <div className="col s6">
                        graphic here
                    </div>
                    <div className="col s6">
                        {semaphore.pressure}
                    </div>
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
