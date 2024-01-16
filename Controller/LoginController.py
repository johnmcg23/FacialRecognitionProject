import boto3
from flask import Flask, Response
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

@app.route('/login', methods=['GET'])
def get_image():
    s3 = boto3.client('s3')

    try:
        file = s3.get_object(Bucket='bucket-name', Key='image-key')
    except NoCredentialsError:
        return "No AWS credentials found", 403

    return Response(
        file['Body'].read(),
        mimetype='image/jpeg',
        headers={"Content-Disposition": "attachment;filename=image.jpg"}
    )

if __name__ == '__main__':
    app.run(debug=True)
