from flask import Flask
import threading
import cv2
import os
import time

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
                cv2.imwrite(filename + extension, img)  # here send it to the S3 bucket
                img_saved = True
                countdown = countdown_start

        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Display
        cv2.imshow('img', img)

        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    # Release the VideoCapture object
    cap.release()