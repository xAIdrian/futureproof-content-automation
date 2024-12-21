import requests
import os
from config import configer
import time
from datetime import datetime, timedelta


def upload_to_instagram(public_url, caption):
    print(f"📧 UPLOAD TO INSTAGRAM: Uploading video to Instagram with caption: {caption}")

    # Load locally saved Instagram token
    with open('instagram_token.txt', 'r') as f:
        access_token = f.read().strip()
    print(f"📧 UPLOAD TO INSTAGRAM: Access token: {access_token}")

    # Step 0: Get Instagram Business Account ID
    account_url = f"https://graph.instagram.com/v21.0/me?fields=user_id,username&access_token={access_token}"
    account_response = requests.get(account_url, timeout=10)

    print("Account Response:", account_response.json())
    instagram_account_id = account_response.json()['user_id']
    
    # Step 1: Create container
    container_params = {
        'media_type': 'REELS',
        'video_url': public_url,
        'caption': caption,
        'access_token': access_token
    }
    container_url = f"https://graph.instagram.com/v21.0/{instagram_account_id}/media"
    
    container_response = requests.post(container_url, data=container_params, timeout=10)
    print("Container Response:",container_response.json())
    conatiner_id = container_response.json()['id']

    # Step 2: Check upload status and if the container is ready to publish
    
    # Set timeout to 5 minutes
    timeout = datetime.now() + timedelta(minutes=5)
    status = "IN_PROGRESS"
    
    while status == "IN_PROGRESS":
        if datetime.now() > timeout:
            raise TimeoutError("Upload status check timed out after 5 minutes")
            
        try:
            status_url = f"https://graph.instagram.com/v21.0/{conatiner_id}?fields=status&access_token={access_token}"
            status_response = requests.get(status_url, timeout=10)
            status_response.raise_for_status()  # Raise exception for non-200 status codes
            
            status_data = status_response.json()
            print("Status Response:", status_data)
            
            if "error" in status_data:
                raise Exception(f"API Error: {status_data['error'].get('message', 'Unknown error')}")
                
            status = status_data.get("status", "UNKNOWN")
            if status == "UNKNOWN":
                raise Exception("Could not determine upload status")
                
            if status != "IN_PROGRESS":
                break
                
            # Wait 5 seconds before checking again
            time.sleep(5)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error while checking upload status: {str(e)}")
    
    # Step 3: Publish the container
    publish_url = f"https://graph.instagram.com/v21.0/{instagram_account_id}/media_publish"
    publish_params = {
        'creation_id': conatiner_id,
        'access_token': access_token
    }
    
    publish_response = requests.post(publish_url, data=publish_params)
    print(publish_response.text)
    
    # Return the URL of the posted content
    post_id = publish_response.json()['id']
    return f"https://www.instagram.com/p/{post_id}"
