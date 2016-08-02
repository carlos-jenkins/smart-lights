import baseapi from './api';

var gridApi = {
    getGrid(callback) {
        baseapi.get('/grid', callback);
    }
};

module.exports = gridApi;
