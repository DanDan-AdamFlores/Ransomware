'use strict'

const MIDDLEWARE = require('./middleware');

let router;

const routing = function routing(express_router) {
	router = express_router;
	
	router.route('/').get(function (req, res) {
		res.json({ message: 'CECS378' });
	});
	router.route('/key').get(function (req, res) {
		MIDDLEWARE.generateAndGetKey(req, res);
	});
	router.route('/key').post(function (req, res) {
		MIDDLEWARE.storeKey(req, res);
	});

	return router;
};

module.exports = routing;
