from flask import Flask
import threading

from facialRecognition import main

app = Flask(__name__)


@app.route('/login/faceid', methods=['GET'])
def GetFaceImageFromS3Bucket():
    # Start the face recognition in a new thread
    threading.Thread(target=main).start()
    return 'Face recognition for login started!'


if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)
