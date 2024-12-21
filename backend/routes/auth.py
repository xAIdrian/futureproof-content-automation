from flask import Blueprint, request, jsonify
from oauth import get_auth, get_token, get_refresh_token

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/auth/instagram', methods=['POST'])
def auth_instagram():
    '''
    This endpoint receives the auth code and saves it to a local file that is persistent across server restarts.
    '''
    data = request.get_json()
    code = data.get('code')
    with open('instagram_token.txt', 'w') as f:
        f.write(code)
    return jsonify({'success': True})

@auth_routes.route('/auth/tiktok', methods=['GET'])
def auth_tiktok():
    generated_url = get_auth()
    return jsonify({'url': generated_url})

@auth_routes.route('/auth/tiktok/token', methods=['POST'])
def get_tiktok_token_from_url():
    try:
        data = request.get_json()
        code = data.get('code')
        
        if not code:
            return jsonify({'error': 'Code is required'}), 400

        access_token, refresh_token, open_id = get_token(code)

        return jsonify({
            'success': access_token is not None and refresh_token is not None and open_id is not None,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'open_id': open_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@auth_routes.route('/auth/tiktok/refresh', methods=['POST'])
def refresh_tiktok_token():
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    return jsonify(get_refresh_token(refresh_token))

@auth_routes.route('/auth/instagram/refresh', methods=['POST'])
def refresh_instagram_token():
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    return jsonify(get_refresh_token(refresh_token))
