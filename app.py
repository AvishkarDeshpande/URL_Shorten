from flask import Flask, request, jsonify, redirect
from flask_pymongo import PyMongo
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import os
import string
import random
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
urls_collection = mongo.db.urls

# Rate Limiting
limiter = Limiter(get_remote_address, app=app, default_limits=["100 per minute"])

def generate_short_id():
    """Generate a unique shortId."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

@app.route('/shorten_the_given_url', methods=['POST'])
@limiter.limit("10 per minute")
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    if not original_url.startswith(('http://', 'https://')):
        return jsonify({'error': 'Invalid URL format'}), 400

    short_id = generate_short_id()
    urls_collection.insert_one({
        "shortId": short_id,
        "originalUrl": original_url,
        "clicks": 0,
        "lastAccessed": None
    })

    return jsonify({'short_url': f'{request.host_url}{short_id}'})

@app.route('/<short_id>', methods=['GET'])
def redirect_to_original(short_id):
    print(f"Looking for short URL: {short_id}")  # Log the shortId received

    # Finding the Mongodb Document
    url_data = urls_collection.find_one({"shortId": short_id})

    # If no URL data is found, return error
    if not url_data:
        return jsonify({'error': 'Short URL not found'}), 404

    # found url
    print(f"Found URL data: {url_data}")

    # Update the clicks and last accessed time
    urls_collection.update_one(
        {"shortId": short_id},
        {"$inc": {"clicks": 1}, "$set": {"lastAccessed": datetime.utcnow()}}
    )

    # redirecting to original url
    print(f"Redirecting to: {url_data['originalUrl']}")  # Log the URL being redirected to

    # Redirect to the original URL
    return redirect(url_data["originalUrl"])


@app.route('/data_given/<short_id>', methods=['GET'])
def get_stats(short_id):
    url_data = urls_collection.find_one({"shortId": short_id})
    if not url_data:
        return jsonify({'error': 'Short URL not found'}), 404

    stats = {
        "shortId": short_id,
        "originalUrl": url_data["originalUrl"],
        "clicks": url_data["clicks"],
        "lastAccessed": url_data["lastAccessed"]
    }
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
