import request from 'superagent';

var baseUrl = 'http://localhost:3001';

var apiService = {
    get: function(url, callback) {
        request
           .get(baseUrl + url)
           .set('Accept', 'application/json')
           .end(function(err, res) {
               callback(err, JSON.parse(res.text))
           });
    },

    put: function(url, params, callback) {

    },
    post: function(url, params, callback) {

    }
};

module.exports = apiService;
