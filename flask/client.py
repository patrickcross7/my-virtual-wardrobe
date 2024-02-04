import base64
import json                    

import requests
from io import BytesIO
from PIL import Image
# THIS CODE IS AN EXAMPLE OF HOW TO GET THE IMAGES FROM MONGODB CONVERT TO PNG
res = requests.get("http://localhost:4000/db/shirts")

print(res.json()[2]['image'])


im_b64 = res.json()[2]['image']
img_bytes = base64.b64decode(im_b64)

# convert bytes data to PIL Image object
img = Image.open(BytesIO(img_bytes))


img.save("test.png", format="png")

