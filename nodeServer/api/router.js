'use strict'

const MIDDLEWARE = require('./middleware');

let router;

const routing = function routing(express_router) {
	router = express_router;
	//Routes
	router.route('/').get(function (req, res) {
		res.json({ message: 'CECS378' });
	});
	//Checks the JWT and public key and sends the private key
	router.route('/key').get(function (req, res) {
		MIDDLEWARE.storePrivGenAppkey(req, res);
	});
	//Stores the keys and returns a JWT for authentication later
	router.route('/key').post(function (req, res) {
		MIDDLEWARE.retrievePriv(req, res);
	});

	return router;
};

module.exports = routing;
