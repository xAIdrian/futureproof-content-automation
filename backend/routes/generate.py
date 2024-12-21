from flask import Blueprint, request, jsonify
from image_gen import draw_conversation
from ai_gen import generate_conversation, generate_image
from movie_gen import create_video
from ig_poster import upload_to_instagram
from cloud_storage import upload_to_gcs
from tiktok_poster import init_video_upload, upload_video_chunk, check_post_status
from routes.setter import convo_data, avatar_data
import os
from werkzeug.utils import secure_filename

generate_routes = Blueprint('generate', __name__)

temp_video_path = None

@generate_routes.route('/image', methods=['GET'])
def generater_image():
    
    image_url = generate_image(convo_data['convo'])
    return jsonify({'image_url': image_url}), 200

@generate_routes.route('/convo', methods=['POST'])
def generate():
    data = request.get_json()
    topic = data.get('topic')
    turns = data.get('turns', 12)

    if not topic:
        return jsonify({'error': 'Information is required'}), 400
    
    # conversation_data = [{'speaker': 'Person 1', 'message': 'Do you believe in love at first sight?', 'timestamp': '11:00 AM'}, {'speaker': 'Person 2', 'message': 'Yes, I think it can happen.', 'timestamp': '11:02 AM'}, {'speaker': 'Person 1', 'message': "That's interesting. I feel the same way.", 'timestamp': '11:04 AM'}, {'speaker': 'Person 2', 'message': "It's a beautiful thing, isn't it?", 'timestamp': '11:06 AM'}, {'speaker': 'Person 1', 'message': 'Yes, it surely is.', 'timestamp': '11:08 AM'}]
    conversation_data = generate_conversation(topic, turns)
    return jsonify(conversation_data), 200

@generate_routes.route('/movie', methods=['POST'])
def generate_movie():

    # return jsonify({'cloud_url': "https://storage.googleapis.com/porygon-video-generation_cloudbuild/reels/20241111_163834__conversation_instagram.mp4"}), 200
    print(convo_data)
    print(avatar_data)
    try:    
        images_list = draw_conversation(convo_data['convo'], avatar_data['avatar_name'], avatar_data['file_name'])
        temp_video_path = create_video(images_list)
        cloud_video_path = upload_to_gcs(temp_video_path)
        return jsonify({'cloud_url': cloud_video_path}), 200

    except Exception as e:
        print('🚩 ~ file: init.py:113 ~ e:', e);
        # Clean up the temp file if there's an error
        if 'temp_video_path' in locals():
            try:
                os.remove(temp_video_path)
            except:
                pass
        return jsonify({'error': str(e)}), 500

@generate_routes.route('/poster', methods=['POST'])
def generate_poster():
    cloud_video_path = None

    data = request.get_json()
    caption = data.get('caption')
    post_to_ig = data.get('post_to_ig', False)
    post_to_tiktok = data.get('post_to_tiktok', False)
    tiktok_access_token = data.get('tiktok_access_token')
    
    if post_to_ig:
        instagram_url = upload_to_instagram(cloud_video_path, caption)
        print(f"♻️ GENERATE: Instagram URL: {instagram_url}")

    if post_to_tiktok:
        publish_id, upload_url = init_video_upload(tiktok_access_token, temp_video_path, caption)
        upload_success = upload_video_chunk(upload_url, temp_video_path)
        status_response = check_post_status(tiktok_access_token, publish_id)

    response = jsonify({
        'cloud_url': cloud_video_path
    })
    return response

@generate_routes.route('/complete-tiktok', methods=['POST'])
def complete_video_to_tiktok_post():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        
        publish_id, upload_url = init_video_upload(tiktok_access_token, file_path, caption)
        upload_success = upload_video_chunk(upload_url, file_path)
        status_response = check_post_status(tiktok_access_token, publish_id)

    else:
        return jsonify({'error': 'Invalid file type'}), 400
    