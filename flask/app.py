from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import io
import PIL.Image as Image
import base64
import gridfs




app = Flask(__name__)
CORS(app)
# uri = "mongodb+srv://admin:admin@hackviolet.pko9vmw.mongodb.net/?retryWrites=true&w=majority"
# db_name = "db"
# #client = pymongo.MongoClient(uri, server_api=pymongo.server_api('1'))


# mongo_client= pymongo.MongoClient("mongodb+srv://admin:admin@hackviolet.pko9vmw.mongodb.net/?retryWrites=true&w=majority")
# db = pymongo.database.Database(mongo_client, db_name)
# collection = db['test']
# cursor = collection.find({})
# for document in cursor:
#     print(document)
# print("connected")

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://admin:admin@hackviolet.pko9vmw.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# database = db[dbName]
# print("Connected to the MongoDB database!")


def shutdown_db_client():
    app.mongodb_client.close()


@app.route("/", methods=["GET"])
def get_all():

    return jsonify("Hello")

@app.route("/insert", methods=["POST"])
def insert():
    im_b64 = request.data
    img_bytes = base64.b64decode(im_b64)

    # convert bytes data to PIL Image object
    img = Image.open(io.BytesIO(img_bytes))


    img.save("test.png", format="png")
    
    return "success"



if __name__ == '__main__':

    app.run(host="0.0.0.0", port="4000")
    shutdown_db_client()



