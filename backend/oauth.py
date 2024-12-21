import requests
import secrets
import urllib
from flask import Flask, jsonify
from flask_cors import CORS

from config import configer

app = Flask(__name__)
CORS(app)

auth_url = 'https://www.tiktok.com/v2/auth/authorize/'

def get_refresh_token(refresh_token):
    try:
        if not refresh_token:
            return jsonify({'error': 'Refresh token is required'}), 400

        # Get client credentials from environment
        client_key = configer['TIKTOK_CLIENT_KEY']
        client_secret = configer['TIKTOK_CLIENT_SECRET']

        # Prepare request data
        data = {
            'client_key': client_key,
            'client_secret': client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        # Make request to TikTok API
        response = requests.post(
            'https://open.tiktokapis.com/v2/oauth/token/',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cache-Control': 'no-cache'
            },
            data=data,
            timeout=10
        )

        response_data = response.json()

        # Check for error in response
        if 'error' in response_data:
            return {
                'error': response_data.get('error'),
                'error_description': response_data.get('error_description')
            }

        # Return new tokens and related data
        return {
            'access_token': response_data.get('access_token'),
            'refresh_token': response_data.get('refresh_token'),
            'expires_in': response_data.get('expires_in'),
            'refresh_expires_in': response_data.get('refresh_expires_in'),
            'open_id': response_data.get('open_id'),
            'scope': response_data.get('scope')
        }

    except Exception as e:
        return {'error': str(e)}

def get_tiktok_auth_token(code):
    '''
    get the auth token with our endpoint redirect url.
    '''
    open_url = 'https://open.tiktokapis.com/v2/oauth/token/'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache'
    }
    
    data = {
        'client_key': configer['TIKTOK_CLIENT_KEY'],
        'client_secret': configer['TIKTOK_CLIENT_SECRET'], 
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': configer['TIKTOK_REDIRECT_URI']
    }
    
    response = requests.post(open_url, headers=headers, data=data, timeout=10)
    print('authentication response: ', response.json())
    return response.json()

def generate_auth_url():
    '''
    generate the auth url that we will send to the user to login with
    '''
    csrf_token = secrets.token_hex(16)
    params = {
        'client_key': configer['TIKTOK_CLIENT_KEY'],
        'redirect_uri': configer['TIKTOK_REDIRECT_URI'],
        'response_type': 'code',
        'scope': 'video.publish',
        'state': csrf_token
    }
    url = auth_url + '?' + urllib.parse.urlencode(params)
    return url

def get_auth():
    return generate_auth_url()

def get_token(code):
    '''
    the url we generate here is manually navigated to by the user and then the code is sent back to us by cutting from the search bar.  Not ideal.
    '''
    json_response = get_tiktok_auth_token(code)
    print('🚀 ~ file: oauth.py:108 ~ json_response:', json_response);
    access_token = json_response['access_token']
    refresh_token = json_response['refresh_token']
    open_id = json_response['open_id']

    return access_token, refresh_token, open_id


if __name__ == "__main__":
    app.run(debug=True, port=5000)


# user will call in from the client, we need to have a flask endpoint that will recquest the initial login information

# we will then send the oauth information to the client, from there the user will be directed to the redirect url

# we will take that url and extract the code in the client

# we will then send that code to our backend and we will use that code to get the access token and refresh token

# this will be stored locally for subsequent requests until an error is thrown.
