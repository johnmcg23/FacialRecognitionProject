from flask import Flask, jsonify, request
import threading

from LoginFaceIdRecognition import main as login_main
from SignUpFaceId import main as signup_main

app = Flask(__name__)


@app.route('/login/faceid/<username>', methods=['POST', 'GET'])
def runFacialRecognitionLogin(username):
    print("Gets in method in python")

    # Start the face recognition in a new thread
    threading.Thread(target=login_main, args=(username,)).start()

    return jsonify('message: Please wait while we scan your face...', 'result')


@app.route('/signup/faceid/<username>', methods=['GET', 'POST'])
def runFacialRecognitionSignUp(username):
    # Start the face recognition in a new thread
    threading.Thread(target=signup_main, args=(username,)).start()

    return jsonify({'message': 'Please wait while we scan your face...'})


if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)
