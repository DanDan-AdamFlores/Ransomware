const mongoose = require('mongoose');

//The User Schema object
const KeySchema = new mongoose.Schema({
	appKey: {
		type: String,
		unique: true,
		required: true
	},
	privateKey = {
		type: Object,
		required: true
	}
});

//Authenticates if the user exists in the database
KeySchema.statics.authentication = function(appKey, callback) {
	this.findOne({appKey: appKey}).exec(function(err, key) {
		if(err) {
			return callback(err);
		} else if (!key) {
			let err = new Error('Application Key not found!');
			err.status = 401;
			return callback(err);
		}
		//The app key exists, return the private Key object
		return callback(null, key.privateKey);
};

const Key = mongoose.model('Key', KeySchema);
module.exports = Key;
