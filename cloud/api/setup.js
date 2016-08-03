#!/usr/bin/env node

var rethinkDB = require('rethinkdb');
require('rethinkdb-init')(rethinkDB);

var connection = null;

function initDb() {
    rethinkDB.connect({ host: 'localhost', port: 28015 }, function(err, conn) {
        if (err) throw err;

        connection = conn;

        rethinkDB.dbList().contains('open_semaphore')
            .do(function(databaseExists) {
                return rethinkDB.branch(
                    databaseExists,
                    { dbs_created: 0 },
                    rethinkDB.dbCreate('open_semaphore')
                );
            }).run(connection, function() {
                checkIfTableExists('semaphore', insertData);
            });

    });
}

function checkIfTableExists(table, callback) {
    rethinkDB.db('open_semaphore').tableList().contains('semaphore')
        .do(function(tableExists) {
            return rethinkDB.branch(
                tableExists,
                { tables_created: 0 },
                rethinkDB.db('open_semaphore').tableCreate(table)
            );
        }).run(connection, callback);
}


function insertData() {
    console.log('Inserting data into DB')
    rethinkDB.db('open_semaphore').table('semaphore').insert([
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

initDb();
