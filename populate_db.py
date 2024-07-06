import subprocess
import json
import random
import time
import requests
from PIL import Image
from io import BytesIO
url = "http://localhost:3000/api/datasets"

def get_image_url(description):
    response = requests.get("https://picsum.photos/300/300")
    image = Image.open(BytesIO(response.content))
    image.show()  # Opens the image
    return response.url

with open('datasets_info.json') as f:
    datasets_info = json.load(f)
    for dataset in datasets_info:
        description = dataset["description"].replace("\n", " ").replace("\t", " ").replace("huggingface.com",
                                                                                           "openmarket ")

        # Generate a random image URL
        generated_image_url = get_image_url(description)
        payload = json.dumps({
            "title": dataset["id"],
            "description": description,
            "authorId": "0xd7b6202152ff734176BCf36bc0D646547684B29d",
            "price": max(10 * random.randint(1, 10), 1),
            "downloads": dataset["downloads"],
            "image": generated_image_url,
            "files": dataset["downloadUrls"]
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=payload)
        print(response.text)

print("Done")



