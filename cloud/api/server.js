var express = require('express');
var cors = require('cors')

var app = express();
app.use(cors());

app.get('/grid', function(req, res) {
    res.json([
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
    ])
});

app.get('/', function (req, res) {
    res.json({data: 'Hello Semaphore'});
});

app.listen(3001, function () {
    console.log('Open Semaphore listening on port 3001! :)');
});
