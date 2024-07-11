

import os
from datetime import datetime
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request, redirect, session, url_for
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
import urllib.parse
import json
from recommendation_engine import generate_recommendations
load_dotenv('API_keys.env')

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://localhost:5173"}})

@app.route('/')
def index():
    return ("http://localhost:5173")

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email playlist-read-private playlist-read-collaborative'  
    params = {
        'client_id': os.environ.get('CLIENT_ID'),
        'response_type': 'code', 
        'scope': scope,
        'redirect_uri': os.environ.get('REDIRECT_URI'),
        'show_dialog': True,
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    print("Redirect URI being used:", params['redirect_uri'])  # Add this line
    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': os.environ.get('REDIRECT_URI'),
            'client_id': os.environ.get('CLIENT_ID'),
            'client_secret': os.environ.get('CLIENT_SECRET')
        }
    
    response = requests.post(TOKEN_URL, data = req_body)
    token_info = response.json()

    session['access_token'] = token_info['access_token']
    session['refresh_token'] = token_info['refresh_token']
    session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

    
    frontend_url = "http://localhost:5173"  # Adjust this to your React app's URL
    redirect_url = f"{frontend_url}?access_token={token_info['access_token']}"
    return redirect(redirect_url)

    


@app.route('/playlists')
def get_playlists():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
    playlists = response.json()

    with open('user_playlists.json', 'w') as outfile:
        json.dump(playlists, outfile)

    return jsonify(playlists)

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session: 
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': os.environ.get('CLIENT_ID'),   
            'client_secret': os.environ.get("CLIENT_SECRET")
        }

        response = requests.post(TOKEN_URL, data = req_body)
        new_token_info = response.json()

        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']\
        
        return redirect('/playlists')

@app.route('/api/get_track_recommendations/<string:playlist_id>', methods = ['GET'])
def get_track_recommendations(playlist_id):
    data = generate_recommendations(playlist_id)
    return data


if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug= True)
