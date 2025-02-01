import base64
import io
import numpy as np
from PIL import Image
from deepface import DeepFace
import os

authorised_faces = "authorised_faces"


def handler(event, context):
    try:
        img_data = event["body"]["image"]
        img_data = img_data.split(",")[1]
        img_bytes = base64.b64decode(img_data)
        img = Image.open(io.BytesIO(img_bytes))

        open_cv_image = np.array(img)
        frame = open_cv_image[:, :, ::-1].copy()

        result = DeepFace.find(frame, db_path=authorised_faces, model_name="ArcFace")

        if len(result) > 0:
            name = result[0]["identity"][0].split("\\")[-1].split(".")[0]
            return {
                "statusCode": 200,
                "body": {
                    "message": f"Hi {name}, You are recognised and successfully authenticated"
                },
            }
        else:
            return {
                "statusCode": 400,
                "body": {"message": "Unknown face! Please register first."},
            }
    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": {"message": "Sorry, error from our side"}}
