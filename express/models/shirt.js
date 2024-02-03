
// Import mongoose library
const mongoose = require('mongoose');

// Create schema
const shirtSchema = new mongoose.Schema({
    title: String,
    description: String,
    image: Buffer,
    season: String,

}, {versionKey: false });

// Export schema
module.exports = mongoose.model('shirts', shirtSchema);
