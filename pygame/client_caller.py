import base64
import json

import requests
from io import BytesIO
from PIL import Image

# THIS CODE IS AN EXAMPLE OF HOW TO GET THE IMAGES FROM MONGODB CONVERT TO PNG


def get_chest():
    res = requests.get("http://localhost:4000/db/currshirt")
    print(res.json())
    im_b64 = res.json()[0]["image"]
    img_bytes = base64.b64decode(im_b64)
    # # convert bytes data to PIL Image object
    img = Image.open(BytesIO(img_bytes))
    img.save("images/chest_image.png", format="png")


def get_legs():
    res = requests.get("http://localhost:4000/db/currshirt")
    print(res.json())
    im_b64 = res.json()[0]["image"]
    img_bytes = base64.b64decode(im_b64)
    # # convert bytes data to PIL Image object
    img = Image.open(BytesIO(img_bytes))
    img.save("images/leg_image.png", format="png")
