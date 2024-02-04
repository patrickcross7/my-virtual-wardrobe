
// Import mongoose library
const mongoose = require('mongoose');

// Create schema
const shirtSchema = new mongoose.Schema({
    title: String,
    image: String,
    season: String,
    created: { type: Date, default: Date.now }

}, {versionKey: false });

// Export schema
module.exports = mongoose.model('shirts', shirtSchema);
