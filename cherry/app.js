
/**
 * Module dependencies.
 */

var express = require('express')
  , routes = require('./routes')
  , user = require('./routes/user')
  , http = require('http')
  , path = require('path');

var app = express();
var sys=require('sys');

// all environments
app.set('port', process.env.PORT || 3000);
app.set('views', __dirname + '/views');
app.set('view engine', 'jade');
app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.bodyParser());
app.use(express.methodOverride());
app.use(app.router);
app.use(express.static(path.join(__dirname, 'public')));


// development only
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

app.get('/', routes.index);
app.post('/incoming', function(req, res) {
var message = req.body.Body;
var from = req.body.From;
sys.log('From: ' + from + ', Message: ' + message);

               var twiml = '<?xml version="1.0" encoding="UTF-8" ?>n<Response>n<Sms>Gracias, su ticket se procesara pronto.</Sms>n</Response>';

               res.send(twiml, {'Content-Type':'text/xml'}, 200);
});

app.get('/users', user.list);

http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
});
