from flask import Flask
import threading
import cv2
import os
import time
import requests
import base64
import requests

app = Flask(__name__)

def main():
    # Load the cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # To capture video from webcam
    cap = cv2.VideoCapture(0)
    img_saved = False

    # Countdown parameters
    countdown_start = 1
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

        # If a face is detected and an image hasn't been saved yet
        if len(faces) > 0 and not img_saved:
            # Display the countdown
            cv2.putText(img, str(countdown), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # If a second has passed
            if time.time() - start_time >= 1:
                countdown -= 1
                start_time = time.time()

            # If the countdown has finished
            if countdown < 0:
                # Check if the file exists and increment the filename if it does
                filename = 'user_face'
                extension = '.png'
                i = 0
                while os.path.exists(filename + extension):
                    i += 1
                    filename = 'user_face_' + str(i)

                # Save the image
                cv2.imwrite(filename + extension, img)

                # Call the new function to upload the image to GitHub
                upload_to_github(filename + extension)
                cap.release()
                return


def upload_to_github(filename):
    # Convert the image to base64
    with open(filename, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode()

    # Set your personal access token, repo, and owner
    token = os.getenv('GITHUB_TOKEN')
    owner = 'johnmcg23'
    repo = 'ImagesForAI'

    # Set the headers for the API request
    headers = {
        'Authorization': 'token ' + token,
        'Accept': 'application/vnd.github.v3+json'
    }

    # Set the data for the API request
    data = {
        'message': 'Add image',
        'content': img_base64
    }

    # Make the API request
    response = requests.put(f'https://api.github.com/repos/{owner}/{repo}/contents/{filename}', headers=headers,
                            json=data)

    # Check the response
    if response.status_code == 201:
        print('Image uploaded to GitHub')
    else:
        print('Failed to upload image to GitHub')

    # Delete the file
    if os.path.exists(filename):
        os.remove(filename)
        print('File deleted')
    else:
        print("The file does not exist")

