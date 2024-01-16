from flask import Flask
import threading

from facialRecognition import main

app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def PostFaceImageToS3Bucket():
    # Start the face recognition in a new thread
    threading.Thread(target=main).start()
    return 'Face recognition started!'

if __name__ == '__main__':
    app.run(debug=True)
