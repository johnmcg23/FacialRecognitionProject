from flask import Flask

app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def PostFaceImageToS3Bucket():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)