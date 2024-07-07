import uuid
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def allowed_file_for_thumbnail(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


@app.route('/test', methods=['GET'])
def get_data():
    return jsonify({"data": "Hello, World!"})


@app.route('/single_image', methods=['POST'])
def upload_single_image():
    print(request.files)
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    current_uuid = str(uuid.uuid4())
    file_ending = file.filename.split('.')[-1]
    this_file_name = current_uuid + '.' + file_ending
    print(this_file_name)
    print(file)
    print(file.filename)
    if file and allowed_file_for_thumbnail(file.filename):
        filename = file.filename

        # create folder if not exists
        if not os.path.exists('data/img/'):
            os.makedirs('data/img/')
        save_path = os.path.join('data/img/', this_file_name)
        # Save the file
        file.save(save_path)

        return jsonify({'message': 'File successfully uploaded', 'uuid': current_uuid, 'filename': this_file_name}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400


# img/uuid?=
# curl 'http://10.190.26.74:5000/retrieve_img_by_uuid?uuid=5e519090-b7e4-4a91-85a5-6389727a4d1e'
@app.route('/retrieve_img_by_uuid', methods=['GET'])
def retrieve_img_by_uuid():
    uuid = request.args.get('uuid')
    if not uuid:
        return jsonify({'error': 'UUID parameter is missing'}), 400

    for file in os.listdir('data/img/'):

        if uuid in file:
            print(file)
            return send_file(os.path.join('data/img/', file))
    return jsonify({'error': 'Image not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
