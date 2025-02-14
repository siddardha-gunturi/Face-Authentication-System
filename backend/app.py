import base64
import io
from flask import Flask, render_template, request, jsonify
from deepface import DeepFace
import os
import numpy as np
import time
from PIL import Image

os.environ["CUDA_VISIBLE_DEVICES"] = "-1" 
app = Flask(__name__, template_folder="../frontend", static_folder="../frontend")
authorised_faces = "authorised_faces"

# create authorised faces path when it doesn't exist
if not os.path.exists(authorised_faces):
    os.makedirs(authorised_faces)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/capture_face", methods=["POST"])
def capture_and_store_new_face():
    # name = input("Please enter your name ")
    image = request.form["image"]
    image = image.split(",")[1]
    image_bites = base64.b64decode(image)

    image = Image.open(io.BytesIO(image_bites))
    name = request.form["name"]
    # if not name:
    #     return jsonify({"error":"Name is required"}),400

    # capture = cv2.VideoCapture(0)
    # time.sleep(2)
    # print("capturing new face " + name)

    # while True:
    #     ret, frame = capture.read()
    #     if not ret:
    #         capture.release()
    #         return jsonify({'error':"Unable to capture"}),500

    # cv2.imwrite(f"{authorised_faces}/{name}.jpg", frame)
    image.save(f"{authorised_faces}/{name}.jpg")
    print(name + " image saved")
    return jsonify({"message": "Face Successfully registered for " + name}), 200


@app.route("/recognize_face", methods=["POST"])
def recognize_face():
    # capture = cv2.VideoCapture(0)
    # time.sleep(3)

    # ret, frame = capture.read()
    # if not ret:
    #     capture.release()
    #     return jsonify({'error':"Unable to capture"}),500

    img_data = request.form["image"]

    img_data = img_data.split(",")[1]
    img_bytes = base64.b64decode(img_data)
    img = Image.open(io.BytesIO(img_bytes))

    open_cv_image = np.array(img)
    frame = open_cv_image[:, :, ::-1].copy()

    try:
        result = DeepFace.find(frame, db_path=authorised_faces, model_name="VGG-Face")

        if len(result) > 0:
            name = result[0]["identity"][0].split("\\")[-1].split(".")[0]
            return (
                jsonify(
                    {
                        "message": "Hi "
                        + name
                        + " You are recognised and successfully authenticated"
                    }
                ),
                200,
            )
        else:
            print("Face not recognized!")
            return jsonify({"message": "Unknown face!!.. register first"}), 400
    except:
        return jsonify({"message": "Sorry error from our side"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway provides the port via the PORT environment variable
    app.run(debug=True, host="0.0.0.0", port=port)

# Face Authentication system
# try:
#     print("Did you authenticate for this system? type Y for Yes and N for No case insensitive")
#     reply = input()
#     if(reply.lower() == 'y'):
#         print("Get ready for authorising yourself")
#         recognize_face()
#     elif(reply.lower() == 'n'):
#         print("You are late but no worries!! You can do that now. ")
#         capture_and_store_new_face()
#     else:
#         print("Please enter valid character")
# except Exception as e:
#     print(e)

# capture_and_store_new_face()
