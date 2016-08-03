import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, browserHistory } from 'react-router';
import App from './App';
import Dashboard from './Dashboard';
import './index.css';

ReactDOM.render(
  (<Router history={browserHistory}>
    <Route path="/" component={App}/>
    <Route path="/dashboard/:semaphoreId" component={Dashboard}/>
  </Router>),
  document.getElementById('root')
);
