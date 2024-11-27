
Here’s a README.md file tailored for your assignment requirements:

URL Shortener API
This is a simple URL shortener backend application built using Flask and MongoDB. The application allows users to shorten URLs, retrieve the original URL, and view usage statistics.

Features
Shorten long URLs into unique short URLs.
Redirect to the original URL using the shortened link.
View statistics for each shortened URL:
Total number of clicks.
Last accessed timestamp.
Rate limiting to prevent abuse (10 requests per minute for shortening URLs).
Prerequisites
Before running the application, ensure you have the following installed:

Python (>=3.7)
MongoDB (Atlas or Local instance)
A package manager like pip

Installation and Setup
1. Clone the Repository
git clone https://github.com/your-repo/url-shortener-api.git
cd url-shortener-api

2. Install Dependencies
pip install -r requirements.txt

4. Set Up Environment Variables
Create a .env file in the root directory and add your MongoDB connection string:
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>

4. Run the Application
Start the server:
python app.py
The server will be available at http://127.0.0.1:5000.

API Endpoints
1. POST /shorten
Shorten a given URL.

Request:
{
  "url": "https://example.com"
}

Response:
{
  "short_url": "http://127.0.0.1:5000/abc123"
}

2. GET /:shortId
Redirect to the original URL using the shortened link.
Request: Access the shortened URL (e.g., http://127.0.0.1:5000/abc123).
Response: Redirects to https://example.com.

4. GET /stats/:shortId
Retrieve statistics for a shortened URL.

Request:
GET /stats/abc123

Response:
{
  "shortId": "abc123",
  "originalUrl": "https://example.com",
  "clicks": 10,
  "lastAccessed": "2024-11-26T18:18:04.229Z"
}
Sample Requests (Using CURL)

Shorten a URL:
curl -X POST -H "Content-Type: application/json" \
-d '{"url": "https://example.com"}' \
http://127.0.0.1:5000/shorten

Redirect to Original URL:
Visit http://127.0.0.1:5000/<shortId> in a browser.

Get Statistics for a Short URL:
curl http://127.0.0.1:5000/stats/<shortId>

Notes
Rate Limiting: The /shorten endpoint is limited to 10 requests per minute.
Use an active MongoDB connection (e.g., MongoDB Atlas) to store and retrieve data.

Deployment
https://url-shorten-962u.onrender.com
