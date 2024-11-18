from flask import Flask, request, jsonify, render_template
from analyze import read_image
from dotenv import load_dotenv
import os

# Initialize the Flask app
app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    # Render the index page
    return render_template('index.html')

# API endpoint at /api/v1/analysis/
@app.route("/api/v1/analysis/", methods=['POST'])
def analysis():
    try:
        # Get the JSON data from the request and extract the URI
        get_json = request.get_json()
        image_uri = get_json.get('uri')

        if not image_uri:
            return jsonify({'error': 'Missing URI in JSON'}), 400
    except Exception as e:
        return jsonify({'error': f'Invalid JSON format: {str(e)}'}), 400

    try:
        # Call the `read_image` function with the provided image URI
        result_text = read_image(image_uri)
        response_data = {
            "text": result_text
        }
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': f'Error in processing: {str(e)}'}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
