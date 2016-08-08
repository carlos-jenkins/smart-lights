var express = require('express');
var cors = require('cors')
var db = require('./database');

var app = express();
app.use(cors());

db.init();

app.get('/grid', function(req, res) {
    db.selectAll('semaphore', function(data) {
        res.json(data)
    });

});

app.get('/all', function(req, res) {
    db.selectAll('semaphore_data', function(data) {
        res.json(data)
    });
});

app.get('/', function (req, res) {
    res.json({data: 'Hello Semaphore'});
});

app.listen(3001, function () {
    console.log('Open Semaphore listening on port 3001! :)');
});
