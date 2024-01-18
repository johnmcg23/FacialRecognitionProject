from flask import Flask, jsonify, request
import threading

from LoginFaceIdRecognition import main as login_main
from SignUpFaceId import main as signup_main

app = Flask(__name__)

from concurrent.futures import ThreadPoolExecutor

# Create a ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=1)


@app.route('/login/faceid/<username>', methods=['GET'])
def runFacialRecognitionLogin(username):
    print("Gets in method in python")

    # Start the face recognition in a new thread and get a Future object
    future = executor.submit(login_main, username)

    # Get the result from the Future
    result = future.result()

    # Return the result
    if result:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route('/signup/faceid/<username>', methods=['POST'])
def runFacialRecognitionSignUp(username):
    print("Getting into sign up backend")
    # Start the face recognition in a new thread
    threading.Thread(target=signup_main, args=(username,)).start()

    return jsonify(True)

if __name__ == '__main__':
    app.run(host='localhost', port=3001, debug=True)
