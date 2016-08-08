var rethinkDB = require('rethinkdb');

var connection = null;

module.exports = {
    init() {
        rethinkDB.connect( {host: 'localhost', port: 28015}, function(err, conn) {
            if (err) {
                throw err;
            }

            connection = conn;
        });
    },
    selectAll(table, callback) {
        rethinkDB.db('smart_lights').table(table).run(connection, function(err, cursor) {
            cursor.toArray(function(err, result) {
                if(err) {
                    return next(err);
                }

                callback(result);
            });
        });
    }
}
