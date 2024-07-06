import os
import json
import uuid
import requests

DATA_DIR = 'data'
IMG_DIR = os.path.join(DATA_DIR, 'img')
README_DIR = os.path.join(DATA_DIR, 'readme_data')

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(README_DIR, exist_ok=True)

def store_data(dataset_id, thumbnails, description, readme_content):
    this_entry_uuid = str(uuid.uuid4())
    print("this_entry_uuid:", this_entry_uuid)

    readme_filename = f'{this_entry_uuid}_{dataset_id}.md'
    readme_path = os.path.join(README_DIR, readme_filename)
    try:
        with open(readme_path, 'w') as readme_file:
            readme_file.write(readme_content)
    except Exception as e:
        print(f"Failed to write to {readme_path}: {e}")
        return  # Optional: Decide if you want to halt on failure

    for thumb in thumbnails:
        thumb_id = thumb['id']
        thumb_url = thumb['url']
        thumb_path = os.path.join(IMG_DIR, f'{this_entry_uuid}_{thumb_id}.jpg')
        try:
            thumb_response = requests.get(thumb_url)
            with open(thumb_path, 'wb') as img_file:
                img_file.write(thumb_response.content)
        except Exception as e:
            print(f"Failed to download or save thumbnail {thumb_id}: {e}")

    all_json_path = os.path.join(DATA_DIR, 'all.json')
    all_data = []

    if os.path.exists(all_json_path):
        try:
            with open(all_json_path, 'r') as all_file:
                all_data = json.load(all_file)
        except json.JSONDecodeError as e:
            print(f"Error reading JSON from {all_json_path}: {e}")

    data_entry = {
        'id': this_entry_uuid,
        'thumbnails': [{'id': thumb['id'], 'url': os.path.join('img', f'{this_entry_uuid}_{thumb["id"]}.jpg')} for thumb in thumbnails],
        'description': description,
        'readme': os.path.join('readme_data', readme_filename)
    }

    all_data.append(data_entry)
    try:
        with open(all_json_path, 'w') as all_file:
            json.dump(all_data, all_file, indent=4)
    except Exception as e:
        print(f"Failed to write to {all_json_path}: {e}")

    print(f"Data stored successfully for {dataset_id}")

def allowed_file_for_thumbnail(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
