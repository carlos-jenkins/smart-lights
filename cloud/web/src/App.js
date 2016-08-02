import React, { Component } from 'react';

import api from './helpers/grid_api';
import './App.css';

class App extends Component {
    componentDidMount() {
        var self = this;
        api.getGrid(function(err, data) {
            self.setState({ markers: data});
        });
    }

    render() {
        console.log(this.state)
        return (
            <div className="App">
                <div className="App-header">
                    <h2>Welcome to Open Semaphore</h2>
                </div>
            </div>
          );
    }
}

export default App;
