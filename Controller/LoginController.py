from flask import Flask, jsonify, request
import threading

from LoginFaceIdRecognition import main

app = Flask(__name__)


@app.route('/login/faceid', methods=['GET'])
def runFacialRecognitionLogin():
    # Get the username from the request
    username = request.json['username']

    # Start the face recognition in a new thread
    threading.Thread(target=main, args=(username,)).start()

    return jsonify({'message': 'Please wait while we scan your face...'})


if __name__ == '__main__':
    app.run(host='localhost', port=3002, debug=True)
