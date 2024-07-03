import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, redirect, session, url_for
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from werkzeug.urls import quote as url_quote

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
CORS(app)

oauth = OAuth(app)

spotify = oauth.remote_app(
    'spotify',
    consumer_key=os.getenv('CLIENT_ID'),
    consumer_secret=os.getenv('CLIENT_SECRET'),
    request_token_params={'scope': 'user-library-read'},
    base_url='https://api.spotify.com/v1/',
    request_token_url=None,
    access_token_url='https://accounts.spotify.com/api/token',
    authorize_url='https://accounts.spotify.com/authorize'
)