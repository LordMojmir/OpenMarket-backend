import uuid

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import requests
import os
import json
from data_storage import store_data, allowed_file_for_thumbnail
from inference import get_response, get_all_possible_models

app = Flask(__name__)
CORS(app)

@app.route('/test', methods=['GET'])
def get_data():
    return jsonify({"data": "Hello, World!"})


@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.json
    dataset_id = data['id']
    thumbnails = data['thumbnails']
    description = data['description']
    readme_content = data['readme']
    store_data(dataset_id, thumbnails, description, readme_content)

    return jsonify({'message': 'Data uploaded successfully'}), 200
@app.route('/single_image', methods=['POST'])
def upload_single_image():
    print(request.files)
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    current_uuid = str(uuid.uuid4())
    this_file_name = current_uuid + '.jpg'
    print(this_file_name)
    print(file)
    print(file.filename)
    if file and allowed_file_for_thumbnail(file.filename):
        filename = file.filename

        save_path = os.path.join('data/img/', this_file_name)
        # Save the file
        file.save(save_path)

        return jsonify({'message': 'File successfully uploaded', 'uuid': current_uuid, 'filename': this_file_name}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400


# img/uuid?=
# curl 'http://127.0.0.1:5000/retrieve_img_by_uuid?uuid=5e519090-b7e4-4a91-85a5-6389727a4d1e'
@app.route('/retrieve_img_by_uuid', methods=['GET'])
def retrieve_img_by_uuid():
    uuid = request.args.get('uuid')
    if not uuid:
        return jsonify({'error': 'UUID parameter is missing'}), 400

    img_path = os.path.join('data/img/', f'{uuid}.jpg')

    if os.path.exists(img_path):
        return send_file(img_path)
    else:
        return jsonify({'error': 'Image not found'}), 404


@app.route('/generate', methods=['POST'])
def generate_response():
    data = request.json
    prompt = data.get('prompt')
    for_model = data.get('model')

    if not prompt or not for_model:
        return jsonify({"error": "Missing prompt or model"}), 400

    try:
        response = get_response(for_model, prompt)
        return jsonify({"prompt": prompt, "response": response})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500

@app.route('/possible_models', methods=['GET'])
def possible_models():
    possible_models = get_all_possible_models()
    return jsonify({"models": possible_models})

def test_route():
    response = app.test_client().get('/api')
    assert response.status_code == 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
