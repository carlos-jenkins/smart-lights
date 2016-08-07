import request from 'superagent';

var baseUrl = 'http://hwthoncr16.herokuapp.com/thegrid';

var api = {
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



module.exports = {
    getLast: function(callback) {
        api.get('/last', function(err, result) {
            if (err) {
                console.log(err);
                return;
            }

            callback(result);
        });
    },

    getAll: function(callback) {
        api.get('/all', function(err, result) {
            if (err) {
                console.log(err);
                return;
            }

            callback(result);
        });
    },

    getLastQty: function(params, callback) {
        api.get('/all', function(err, result) {
            if (err) {
                console.log(err);
                return;
            }
            var length = result.length;
            callback(result.slice(length - params.qty, length));
        });
    }
};
