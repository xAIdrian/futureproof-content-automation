import os
from google.cloud import storage
from datetime import datetime
from google.oauth2.service_account import Credentials

def upload_to_gcs(local_file_path, bucket_name = 'default-automated-marketing-content-bucket'):
    """
    Upload a file to Google Cloud Storage and return the public URL.
    
    Args:
        local_file_path (str): Path to the local file
        bucket_name (str): Name of the GCS bucket
    
    Returns:
        str: Public URL of the uploaded file
    """
    try:
        credentials = Credentials.from_service_account_file(
            'automated-marketing-442414-a14d5676b6c7.json'
        )
        # Initialize the client
        storage_client = storage.Client(credentials=credentials)
        
        # Get the bucket
        bucket = storage_client.bucket(bucket_name)
        
        # Create a unique blob name using timestamp
        blob_name = f"reels/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(local_file_path)}"
        blob = bucket.blob(blob_name)
        
        # Upload the file
        generation_match_precondition = 0
        blob.upload_from_filename(local_file_path, if_generation_match=generation_match_precondition)
        
        # Make the blob publicly accessible
        # blob.make_public()
        
        # Get the public URL
        public_url = blob.public_url
        print(f"File uploaded successfully to: {public_url}")
        return public_url
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise
