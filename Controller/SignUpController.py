from flask import Flask
import threading

from SignUpFaceId import main

app = Flask(__name__)


@app.route('/signup/faceid', methods=['GET', 'POST'])
def PostFaceImageToS3Bucket():
    # Start the face recognition in a new thread
    threading.Thread(target=main).start()
    return 'Face recognition started!'


if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)
