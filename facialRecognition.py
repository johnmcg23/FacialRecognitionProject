import cv2
import face_recognition
import os


def load_known_faces():
    known_faces = []
    known_face_names = []
    for filename in os.listdir('.'):  # Looks in this file for images
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
        print('no match')
        color = (0, 0, 255)  # Red

        # If a match was found in known_faces, use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            print('no match')
            color = (0, 255, 0)  # Green

        face_names.append((name, color))

    return face_locations, face_names


def display_results(frame, face_locations, face_names):
    # Display the results
    for (top, right, bottom, left), (name, color) in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    # cv2.imshow('Video', frame)  # Commented out to prevent window from opening


def main():
    known_faces, known_face_names = load_known_faces()

    # Capture video from the webcam
    video_capture = cv2.VideoCapture(0)

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        face_locations, face_names = process_frame(frame, known_faces, known_face_names)

        display_results(frame, face_locations, face_names)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
