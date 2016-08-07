import React, { Component } from 'react';
import moment from 'moment';

import api from './helpers/grid_api';
import './Dashboard.css';

var semaphore_data = {
    id: 'something-something',
    id_semaphore: 'd17f670c-1cf5-41ff-a2aa-408868910d1c',
    timestamp: Date.now(),
    state: 'red',
    data: {
        noise: 10,
        gas: 40,
        temperature: 26.26,
        pressure: 880.08,
        humidity: 63.16
    }
}

var self;

class Dashboard extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {
            semaphore: semaphore_data,
            active: semaphore_data.state
        }

        self = this;
    }

    componentDidMount() {
        this._timer = setInterval(this._tick, 1000);
    }

    componentWillUnmount() {
        clearInterval(this._timer);
    }

    render() {
        var semaphore = this.state.semaphore;
        var data = semaphore.data;

        console.log(this.state.active);

        return (
            <div className="container">
                <div className="row">
                    <div className="col s6">
                        <h1>Dashboard</h1>
                    </div>
                    <div className="col s6">
                        <h5>{this.state.date}</h5>
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
                    <div className="col s12">
                        <h2>Noise</h2>
                    </div>
                </div>
                <div className="row">
                    <div className="col s6">
                        graphic here
                    </div>
                    <div className="col s6">
                        {data.noise}
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
                        {data.temperature}
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
                        {data.humidity}
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
                        {data.pressure}
                    </div>
                </div>
            </div>
        );
    }

    _tick() {
        self.setState({date: moment().format('MMMM Do YYYY, h:mm:ss a')});
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
