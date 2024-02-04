const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const fs = require("fs");
const Jimp = require("jimp");

require('dotenv').config();
let showShirt = {}
let showPants = {}


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

router.route("/currshirt").get((req, res) => {
	shirtSchema.find().sort({ created: -1 }).limit(1).then(function (items) {
		// console.log(items);
		//find all items are returns
		showShirt = items
		console.log(showShirt)
		res.json(items);
	});

});
router.route("/currpants").get((req, res) => {
	pantsSchema.find().sort({ created: -1 }).limit(1).then(function (items) {
		// console.log(items);
		//find all items are returns
		showPants = items
		// console.log(showShirt)
		res.json(items);
	});


});
//get all shirt entries
router.route("/shirts").get((req, res) => {

	shirtSchema.find().then(function (items) {
		// console.log(items);
		//find all items are returns
		// console.log(items)
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
		item.save()
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
	// console.log(req.body);
	// crop("shirt", req.body.image)
	shirtSchema.create({ title: req.body.title, season: req.body.season, image: req.body.image }).then((item) => {
		console.log(item)
		res.json(item)
	});
});

//create pants entry
router.route("/pants/create").post((req, res) => {
	// console.log(req.body);
	pantsSchema.create({ title: req.body.title, season: req.body.season, leftImage: req.body.leftImage, rightImage: req.body.rightImage }).then((item) => {
		pantsSchema.find().then(function (item) {

			res.json(item)
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



function crop(type, base64) {

	const buffer = Buffer.from(base64, "base64");
	fs.writeFileSync("temp.png", buffer);
	Jimp.read("temp.png")
		.then((lenna) => {
			return lenna
				.resize(256, 256) // resize
				.crop(0, 0, 100, 100)
				.write("temp1.png") // save
		})
		.catch((err) => {
			console.error(err);
		});

}

const port = 4000;
app.listen(port, () => console.log(`Hello world app listening on port ${port}!`));
