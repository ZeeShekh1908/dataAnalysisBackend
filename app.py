from flask import Flask, jsonify,send_from_directory
from flask_cors import CORS
from controllers import get_data
import os

app = Flask(__name__,static_folder='../frontend/build',static_url_path='/')
CORS(app)

# Route for the home page
@app.route('/')
def home():
    return "<h1>Welcome to the Data Visualization Dashboard API</h1>"

# Route for fetching data
@app.route('/api/data', methods=['GET'])
def fetch_data():
    data = get_data()
    return jsonify(data)

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
