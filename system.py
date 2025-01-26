import cv2
from deepface import DeepFace
import os
import numpy as np

authorised_faces = "authorised_faces"

# create authorised faces path when it doesn't exist
if not os.path.exists(authorised_faces):
    os.makedirs(authorised_faces)

def capture_and_store_new_face():
    name = input("Please enter your name ")
    capture = cv2.VideoCapture(0)
    print("capturing new face " + name)
    
    while True:
        ret, frame = capture.read()
        if not ret:
            break

        cv2.imshow("Capture Face", frame)

        if cv2.waitKey(1) & 0xFF == ord(" "):
            cv2.imwrite(f"{authorised_faces}/{name}.jpg", frame)
            print(name + " image saved")
            break

    capture.release()
    cv2.destroyAllWindows()

def recognize_face():
    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        result = DeepFace.find(frame, db_path=authorised_faces)
        # demography = DeepFace.analyze(frame)
        # cv2.putText(frame, str(demography), (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if len(result) > 0:
            name = result[0]["identity"][0].split("\\")[-1].split(".")[0]
            cv2.putText(frame, "Hi "+name+"!!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            print("Face not recognized!")
            cv2.putText(frame, "Unknown Face", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Real-time Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord(" "):
            break

    capture.release()
    cv2.destroyAllWindows()

# Face Authentication system
try: 
    print("Did you authenticate for this system? type Y for Yes and N for No case insensitive")
    reply = input()
    if(reply.lower() == 'y'):
        print("Get ready for authorising yourself")
        recognize_face()
    elif(reply.lower() == 'n'):
        print("You are late but no worries!! You can do that now. ")
        capture_and_store_new_face()
    else:
        print("Please enter valid character")
except Exception as e:
    print(e)

#capture_and_store_new_face()