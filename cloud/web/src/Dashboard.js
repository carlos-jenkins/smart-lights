import React, { Component } from 'react';

import api from './helpers/grid_api';
import './Dashboard.css';

class Dashboard extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = { }
    }

    componentDidMount() {
        var self = this;
    }

    render() {
        return (
            <div className="container">
                <h1>Dashboard</h1>

            </div>
        );
    }
}

export default Dashboard;
