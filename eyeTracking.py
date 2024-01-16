import cv2
import dlib

# Initialize dlib's face detector and create a predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def draw_eye_circle(frame, landmarks, eye_points):
    # Get the coordinates of the eyes
    left_point = (landmarks.part(eye_points[0]).x, landmarks.part(eye_points[0]).y)
    right_point = (landmarks.part(eye_points[3]).x, landmarks.part(eye_points[3]).y)
    center_top = ((landmarks.part(eye_points[1]).x + landmarks.part(eye_points[2]).x) // 2, (landmarks.part(eye_points[1]).y + landmarks.part(eye_points[2]).y) // 2)
    center_bottom = ((landmarks.part(eye_points[5]).x + landmarks.part(eye_points[4]).x) // 2, (landmarks.part(eye_points[5]).y + landmarks.part(eye_points[4]).y) // 2)

    # Draw a circle around the eye
    rad = int(cv2.norm(center_top, center_bottom))
    cv2.circle(frame, center_top, rad, (255, 0, 0), 2)

def main():
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)

            # Draw a circle around the eyes
            draw_eye_circle(frame, landmarks, range(36, 42))  # Left eye
            draw_eye_circle(frame, landmarks, range(42, 48))  # Right eye

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
