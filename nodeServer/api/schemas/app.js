const mongoose = require('mongoose');

const AppSchema = mongoose.Schema({
	appKey: {
		type: String,
		required: true,
		unique: true
	}
});

const App = mongoose.model('App', AppSchema);

module.exports = App;
