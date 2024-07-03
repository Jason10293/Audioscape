from flask import Flask, jsonify, request, redirect, session, url_for
from flask_cors import CORS
from flask_oauthlib.client import OAuth
from Secrets import CLIENT_ID, CLIENT_SECRET, REDIRECT_URL, FLASK_SECRET_KEY

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
CORS(app)

oauth = OAuth(app)

spotify = oauth.remote_app(
    'spotify',
    consumer_key=CLIENT_ID,
    consumer_secret=CLIENT_SECRET,
    request_token_params={'scope': 'user-library-read'},
    base_url='https://api.spotify.com/v1/',
    request_token_url=None,
    access_token_url='https://accounts.spotify.com/api/token',
    authorize_url='https://accounts.spotify.com/authorize'
)