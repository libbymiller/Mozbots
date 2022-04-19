var fs = require('fs'),
    http = require('http'),
    https = require('https'),
    express = require('express');
const { ExpressPeerServer } = require('peer');
var port = 8443;
var options = {
   key: fs.readFileSync('/etc/letsencrypt/live/myserver.example.com/privkey.pem'),
   cert: fs.readFileSync('/etc/letsencrypt/live/myserver.example.com/fullchain.pem')
};
const app = express();
var server = https.createServer(options, app).listen(port, function(){
  console.log("Express server listening on port " + port);
});
app.get('/', (req, res, next) => res.send('Hello world!'));
const peerServer = ExpressPeerServer(server, {
  debug: true,
  path: '/',
  port: port,
  proxied: true,
  allow_discovery: true,
  ssl: {
    key: fs.readFileSync('/etc/letsencrypt/live/myserver.example.com/privkey.pem'),
    cert: fs.readFileSync('/etc/letsencrypt/live/myserver.example.com/fullchain.pem')
  }
});
app.use('/', peerServer);
peerServer.on('connection', function(id) {
   console.log(id)
   //console.log(server._clients)
});
server.on('disconnect', function(id) {
    console.log(id + "deconnected")
});
app.use(express.static('public'))
