const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
require('dotenv').config();
// Set the web server
const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cors());
app.get(
	"/",
	(req, res) => res.send("<h1>HackViolet 2024 Backend</h1>") 
);

// Connect to MongoDB database
mongoose.Promise = global.Promise;
mongoose.connect(process.env.MONGO_URI, {
	useNewUrlParser: true,
	useUnifiedTopology: true,
});
mongoose.connection.once("open", function () {
	console.log("Connection with MongoDB was successful");
});

// Create routes for database access

const shirtSchema = require("./models/shirt")
const pantsSchema = require("./models/pants");


const router = express.Router();
app.use("/db", router);

//get all shirt entries
router.route("/shirts").get((req, res) => {
	shirtSchema.find().then(function (items) {
		// console.log(items);
		//find all items are returns
		res.json(items);
	});
});
//get all pants entries
router.route("/pants").get((req, res) => {

	pantsSchema.find().then(function (items) {
		// console.log(items);
		//find all items are returns
		res.json(items);
	});
});

//update one shirt entry
router.route("/shirt/update/:id").post((req, res) => {
	shirtSchema.findById(req.params.id).then((item) => {
		//need to add in the code here later to update the entry

		item
			.save()
			.then((item) => {
				res.json;
			})
			.catch((err) => {
				res.status(400).send("Update not possible");
			});
	});
});
//update one pants entry
router.route("/pants/update/:id").post((req, res) => {
	pantsSchema.findById(req.params.id).then((item) => {
		//need to add in the code here later to update the entry

		item
			.save()
			.then((item) => {
				res.json;
			})
			.catch((err) => {
				res.status(400).send("Update not possible");
			});
	});
});

//create shirt entry
router.route("/shirts/create").post((req, res) => {
	console.log(req.body);
	shirtSchema.create({"hi": "hi"}).then((item) => {
		shirtSchema.find().then(function (items) {
			// console.log(items);
			//find all items are returns
			res.json(items);
		});
	});
});

//create pants entry
router.route("/pants/create").post((req, res) => {
	// console.log(req.body);
	pantsSchema.create({"hi": "hi"}).then((item) => {
		pantsSchema.find().then(function (items) {
			// console.log(items);
			//find all items are returns
			res.json(items);
		});
	});
});

//delete one shirt endpoint
router.route("/shirts/delete/:id").delete((req, res) => {
    pantsSchema.deleteOne({ _id: req.params.id })
});
//delete one pants endpoint
router.route("/pants/delete/:id").delete((req, res) => {
	// console.log(req.body);
    pantsSchema.deleteOne({ _id: req.params.id })
	
});


const port = 4000;
app.listen(port, () => console.log(`Hello world app listening on port ${port}!`));
