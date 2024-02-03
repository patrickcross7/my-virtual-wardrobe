import base64
import json                    

import requests

api = 'http://localhost:8080/test'
image_file = '../png/one.png'

with open(image_file, "rb") as f:
    im_bytes = f.read()        
im_b64 = base64.b64encode(im_bytes).decode("utf8")

# headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

f = open("base64.txt", "a")
f.write(im_b64)
f.close()
# payload = json.dumps({"image": im_b64, "other_key": "value"})
# response = requests.post(api, data=payload, headers=headers)
# try:
#     data = response.json()     
#     print(data)                
# except requests.exceptions.RequestException:
#     print(response.text)