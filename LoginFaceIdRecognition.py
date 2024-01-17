from datetime import time
from tkinter import Image
import cv2
import face_recognition
import os
import requests
import base64
import io


def load_known_faces(username):
    known_faces = []
    known_face_names = []
    # Use GitHub API to get the content of the repository
    url = f"https://api.github.com/repos/{username}/repo/contents/"
    response = requests.get(url)
    files = response.json()

    for file in files:
        if file['name'].endswith((".png", ".jpg", ".jpeg")):
            # Download the image file
            image_url = file['download_url']
            response = requests.get(image_url)
            image_data = response.content

            # Convert the image data to an image
            image = Image.open(io.BytesIO(image_data))

            face_encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(face_encoding)
            name, ext = os.path.splitext(file['name'])
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

            print('match')
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


def check_in_github(filename):
    # Set your personal access token, repo, and owner
    token = os.getenv('GITHUB_TOKEN')
    owner = 'johnmcg23'
    repo = 'ImagesForAI'

    # Set the headers for the API request
    headers = {
        'Authorization': 'token ' + token,
        'Accept': 'application/vnd.github.v3+json'
    }

    # Make the API request
    response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/contents/{filename}', headers=headers)

    # Check the response
    if response.status_code == 200:
        # The file exists in the repo
        # Now we need to compare the face in the current image with the one in the repo
        # First, we load the image from the repo
        img_base64 = response.json()['content']
        img_data = base64.b64decode(img_base64)
        img = Image.open(io.BytesIO(img_data))

        # Then, we load the current image
        current_img = cv2.imread(filename)

        # We get the face encodings for both images
        repo_face_encoding = face_recognition.face_encodings(img)[0]
        current_face_encoding = face_recognition.face_encodings(current_img)[0]

        # And finally, we compare the faces
        match = face_recognition.compare_faces([repo_face_encoding], current_face_encoding)

        if match[0]:
            print('Face matches')
            return True
        else:
            print('Face does not match')
            return False
    else:
        print('Username does not match')
        return False


def main(username):
    # Load the cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # To capture video from webcam
    cap = cv2.VideoCapture(0)

    # Countdown parameters
    countdown_start = 3
    countdown = countdown_start

    # Record the start time
    start_time = time.time()

    while True:
        # Read the frame
        _, img = cap.read()

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # If a face is detected
        if len(faces) > 0:
            # Display the countdown
            cv2.putText(img, str(countdown), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # If a second has passed
            if time.time() - start_time >= 1:
                countdown -= 1
                start_time = time.time()

            # If the countdown has finished
            if countdown < 0:
                # Save the image with the username
                filename = username + '.png'
                cv2.imwrite(filename, img)

                # Call the new function to check the image in GitHub
                success = check_in_github(filename)

                # Delete the local file
                if os.path.exists(filename):
                    os.remove(filename)

                cap.release()

                return success  # Return boolean value


if __name__ == "__main__":
    main()
