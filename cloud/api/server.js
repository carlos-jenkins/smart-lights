var express = require('express');
var app = express();

app.get('/', function (req, res) {
  res.json({data: 'Hello Semaphore'});
});

app.listen(3001, function () {
  console.log('Open Semaphore listening on port 3001!');
});
