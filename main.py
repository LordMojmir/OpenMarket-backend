from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
import json
from data_storage import store_data, allowed_file_for_thumbnail
from inference import get_response, get_all_possible_models

app = Flask(__name__)
CORS(app)


@app.route('/api', methods=['GET'])
def get_data():
    response = requests.get('https://api.example.com/data')
    return jsonify(response.json())


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
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file_for_thumbnail(file.filename):
        # Use the filename from the uploaded file (consider sanitizing or securing the filename)
        filename = file.filename
        save_path = os.path.join('data', filename)

        # Save the file
        file.save(save_path)

        return jsonify({'message': 'File successfully uploaded', 'filename': filename}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400


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
    app.run()
