import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from routes.auth import auth_routes
from routes.generate import generate_routes
from routes.setter import set_routes
from ai_gen import generate_image
from movie_gen import create_video
from cloud_storage import upload_to_gcs
from image_gen import draw_conversation

def local_screenshot_gen():
    
    # Generate the image
    result = draw_conversation(
        [
            {
                "speaker": "Person 1",
                "message": "Hello, how are you?",
                "timestamp": "12:00 PM"
            },
            {
                "speaker": "Person 2",
                "message": "I'm doing great, thanks for asking!",
                "timestamp": "12:05 PM"
            },
            {
                "speaker": "Person 1",
                "message": "What's your favorite color?",
                "timestamp": "12:10 PM"
            },
            {
                "speaker": "Person 2",
                "message": "I like blue.",
                "timestamp": "12:15 PM"
            }
        ],
        "Porygon",
        "https://oaidalleapiprodscus.blob.core.windows.net/private/org-tuJXby1unexn4gYXiRai41Dr/user-TWNSwCxTcCjFHTglfIpe3wKm/img-Xn5Qyv49VGqPw3OdAZkD3oYn.png?st=2024-11-27T02%3A22%3A09Z&se=2024-11-27T04%3A22%3A09Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-11-27T00%3A16%3A55Z&ske=2024-11-28T00%3A16%3A55Z&sks=b&skv=2024-08-04&sig=uzHqwt1Y5%2BcA6yYp/Xy9Lo%2BdKu4fj7s9OmAG79zB5oY%3D"
    )
    print("Images generated successfully!")
    for i, img in enumerate(result):
        img.show() # This will open each image in the default image viewer
        print(f"Showing image {i+1} of {len(result)}")

def load_movie_send_to_cloud():
    result = draw_conversation(
        [
            {
                "speaker": "Person 1",
                "message": "Hello, how are you?",
                "timestamp": "12:00 PM"
            },
            {
                "speaker": "Person 2",
                "message": "I'm doing great, thanks for asking!",
                "timestamp": "12:05 PM"
            },
            {
                "speaker": "Person 1",
                "message": "What's your favorite color?",
                "timestamp": "12:10 PM"
            },
            {
                "speaker": "Person 2",
                "message": "I like blue.",
                "timestamp": "12:15 PM"
            }
        ],
        "Porygon",
        "https://oaidalleapiprodscus.blob.core.windows.net/private/org-tuJXby1unexn4gYXiRai41Dr/user-TWNSwCxTcCjFHTglfIpe3wKm/img-Xn5Qyv49VGqPw3OdAZkD3oYn.png?st=2024-11-27T02%3A22%3A09Z&se=2024-11-27T04%3A22%3A09Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-11-27T00%3A16%3A55Z&ske=2024-11-28T00%3A16%3A55Z&sks=b&skv=2024-08-04&sig=uzHqwt1Y5%2BcA6yYp/Xy9Lo%2BdKu4fj7s9OmAG79zB5oY%3D"
    )
    temp_video_path = create_video(result, audio_data={
        "audio_file_name": "test.mp3",
        "audio_file_path": "uploads/audio/1732679043-FREE_Dark_Lil_Peep_Type_Beat_-_Enchanted_Curse.mp3"
    })
    cloud_video_path = upload_to_gcs(temp_video_path)
    print(cloud_video_path)


def local_image_gen():
    prompt = "A woman and her sister are discussing their favorite color one of them is wearing a red dress"
    result = generate_image(prompt)
    print(result)

if __name__ == "__main__":
    # local_image_gen()
    # local_screenshot_gen()
    load_movie_send_to_cloud()
