import base64
import io
from PIL import Image
import os
from flask import jsonify

authorised_faces = "authorised_faces"
if not os.path.exists(authorised_faces):
    os.makedirs(authorised_faces)


def handler(event, context):
    try:
        image = event["body"]["image"]
        image = image.split(",")[1]
        image_bytes = base64.b64decode(image)
        image = Image.open(io.BytesIO(image_bytes))
        name = event["body"]["name"]

        image.save(f"{authorised_faces}/{name}.jpg")
        print(f"{name} image saved")

        return {
            "statusCode": 200,
            "body": {"message": f"Face Successfully registered for {name}"},
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": {"message": "Sorry, error on our side"}}
