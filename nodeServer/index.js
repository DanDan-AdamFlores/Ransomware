'use strict'

const MONGOOSE = require('mongoose');
const DB_CONFIG = require('./config/mongo');
const EXPRESS = require('express');
const ROUTES = require('./api/router');
const BODY_PARSER = require('body-parser');
const http = require('http');
const https = require('https');
const fs = require('fs');
const helmet = require('helmet');
const ROUTER = ROUTES(EXPRESS.Router());
const ONE_YEAR = 31536000000;
const httpApp = EXPRESS();
const httpsApp = EXPRESS();

const port = 8080;
const securePort = 3000;

let cipher =  ['ECDHE-ECDSA-AES256-GCM-SHA384',
'ECDHE-RSA-AES256-GCM-SHA384',
'ECDHE-RSA-AES256-CBC-SHA384',
'ECDHE-RSA-AES256-CBC-SHA256',
'ECDHE-ECDSA-AES128-GCM-SHA256',
'ECDHE-RSA-AES128-GCM-SHA256',
'DHE-RSA-AES128-GCM-SHA256',
'DHE-RSA-AES256-GCM-SHA384',
'!aNULL',
'!MD5',
'!DSS'].join(':');

//Redirect Http connection to HTTPS
httpApp.get('*', function(req, res, next) {
	res.redirect('https://' + req.headers.host + req.url);
});

httpsApp.use(helmet.hsts({
	maxAge:ONE_YEAR,
	includeSubdomains: true,
	force: true
}));

httpsApp.use(BODY_PARSER.urlencoded({ extended: true }));
httpsApp.use(BODY_PARSER.json());
httpsApp.use('/', ROUTER);

let options = {
        key: fs.readFileSync(__dirname + '/privkey.pem'),
        cert: fs.readFileSync(__dirname + '/fullchain.pem'),
	ciphers: cipher
};

https.createServer(options, httpsApp).listen(securePort);
http.createServer(httpApp).listen(port);

MONGOOSE.connect(DB_CONFIG.path);

