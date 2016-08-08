#!/usr/bin/env node

var rethinkDB = require('rethinkdb');

var connection = null;

function initDb() {
    rethinkDB.connect({ host: 'localhost', port: 28015 }, function(err, conn) {
        if (err) throw err;

        connection = conn;

        rethinkDB.dbList().contains('smart_lights')
            .do(function(databaseExists) {
                return rethinkDB.branch(
                    databaseExists,
                    { dbs_created: 0 },
                    rethinkDB.dbCreate('smart_lights')
                );
            }).run(connection, function() {
                checkIfTableExists('semaphore', insertData);
                checkIfTableExists('semaphore_data', insertSemaphoreData);
            });

    });
}

function checkIfTableExists(table, callback) {
    rethinkDB.db('smart_lights').tableList().contains('semaphore')
        .do(function(tableExists) {
            return rethinkDB.branch(
                tableExists,
                { tables_created: 0 },
                rethinkDB.db('smart_lights').tableCreate(table)
            );
        }).run(connection, callback);
}


function insertData() {
    console.log('Inserting data into DB')
    rethinkDB.db('smart_lights').table('semaphore').insert([
        {
            latitude: 9.9454167,
            longitude: -84.1491331,
            name: 'Multiplaza del Este'
        },
        {
            latitude: 9.9412773,
            longitude: -84.082515,
            name: 'Museo de los Niños'
        }
    ]).run(connection, function(err, result) {
        console.log(JSON.stringify(result, 0, 2));
        console.log('Data inserted into semaphore table.')
        process.exit(0);
    });
}

function insertSemaphoreData() {
    console.log('Inserting data into DB')
    rethinkDB.db('smart_lights').table('semaphore_data').insert(require('./dumpData')).run(connection, function(err, result) {
        console.log(JSON.stringify(result, 0, 2));
        console.log('Data inserted into semaphore table.')
        process.exit(0);
    });
}

initDb();
