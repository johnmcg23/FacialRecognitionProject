#Does work, however the age bucket is displayed at the top right hand corner rather than on the face

import cv2
import face_recognition
import os

# Load the age prediction model
age_net = cv2.dnn.readNetFromCaffe('deploy_age.prototxt', 'age_net.caffemodel')

# Define the list of age buckets our age detector will predict
AGE_BUCKETS = ["(0-2)", "(4-6)", "(8-12)", "(15-20)", "(25-32)", "(38-43)", "(48-53)", "(60-100)"]

def load_known_faces():
    known_faces = []
    known_face_names = []
    for filename in os.listdir('.'):
        if filename.endswith((".png", ".jpg", ".jpeg")):  # Add more file types if needed
            image = face_recognition.load_image_file(filename)
            face_encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(face_encoding)
            name, ext = os.path.splitext(filename)  # Split the filename and the extension
            known_face_names.append(name)
    return known_faces, known_face_names

def process_frame(frame, known_faces, known_face_names):
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "NO MATCH"
        color = (0, 0, 255)  # Red

        # If a match was found in known_faces, use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            color = (0, 255, 0)  # Green

        face_names.append((name, color))

    return face_locations, face_encodings, face_names

def predict_age(frame, face_locations):
    # Initialize our results list
    results = []

    # Loop over the face detections
    for i in range(0, len(face_locations)):
        # Extract the ROI of the face
        (top, right, bottom, left) = face_locations[i]
        face = frame[top:bottom, left:right]

        # Construct a blob from *just* the face ROI
        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)

        # Predict age
        age_net.setInput(blob)
        age_preds = age_net.forward()
        age = age_preds[0].argmax()

        # Construct a dictionary consisting of both the face bounding box location along with the age prediction, then update our results list
        d = {
            "loc": (top, right, bottom, left),
            "age": AGE_BUCKETS[age]
        }
        results.append(d)

    # Return our results to the calling function
    return results

def display_results(frame, face_locations, face_names, results):
    # Loop over the results
    for r in results:
        # Draw the bounding box of the face along with the associated predicted age
        text = "{}: {}".format(r["loc"], r["age"])
        (top, right, bottom, left) = r["loc"]
        y = top - 10 if top - 10 > 10 else top + 10
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, text, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    # Display the resulting image
    cv2.imshow('Video', frame)

def main():
    known_faces, known_face_names = load_known_faces()

    # Capture video from the webcam
    video_capture = cv2.VideoCapture(0)

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        face_locations, face_encodings, face_names = process_frame(frame, known_faces, known_face_names)
        results = predict_age(frame, face_locations)

        display_results(frame, face_locations, face_names, results)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
