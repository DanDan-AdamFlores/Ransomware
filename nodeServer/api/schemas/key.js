const mongoose = require('mongoose');

const KeySchema = new mongoose.Schema({
	private: {
		type: String,
		required: true
	},
	public: {
		type:String,
		unique: true,
		required: true
	}
});


const Key = mongoose.model('Key', KeySchema);
module.exports = Key;
