// var baseUrl = 'http://hwthoncr16.herokuapp.com/thegrid';
var baseUrl = 'http://localhost:3001';

module.exports = {
    getLast: function(callback) {
        fetch(baseUrl + '/last')
            .then(function(response) {
                return response.json()
            }).then(function(json) {
                callback(json);
            }).catch(function(ex) {
                console.log('parsing failed', ex)
                callback([]);
            })
    },

    getAll: function(callback) {
        fetch(baseUrl + '/all')
            .then(function(response) {
                return response.json()
            }).then(function(json) {
                callback(json);
            }).catch(function(ex) {
                console.log('parsing failed', ex)
            })
    },

    getLastQty: function(params, callback) {
        fetch(baseUrl + '/all')
            .then(function(response) {
                return response.json()
            }).then(function(json) {
                var length = json.length;
                callback(json.slice(length - params.qty, length));
            }).catch(function(ex) {
                console.log('parsing failed', ex)
            })
    },

    setSemaphoreState: function(params, callback) {
        var pythonServer = 'http://192.168.8.100:8080';
        fetch(pythonServer + '/state/' + params.state)
            .then(function(response) {
               return response.json()
            }).then(function(json) {
               callback && callback(json);
            }).catch(function(ex) {
               console.log('parsing failed', ex)
           });
    }
};
