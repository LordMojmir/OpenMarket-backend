import Flask
import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['GET'])
def get_data():
    response = requests.get('https://api.example.com/data')
    return response.json()

def test_route():
    response = app.test_client().get('/api')
    assert response.status_code == 200

if __name__ == '__main__':
    app.run()
