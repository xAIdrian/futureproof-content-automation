import subprocess
import numpy as np
from moviepy.editor import ImageSequenceClip, AudioFileClip
import tempfile
import os
import shutil
from routes.setter import audio_data

def save_with_temp_file(video_file, fps):
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
        temp_path = temp_file.name
        video_file.write_videofile(temp_path, fps=fps, codec='libx264')
    return temp_path

def create_video(images_list, audio_data=None):
    print('📸 ~ file: movie_gen.py:15 ~ images_list:', len(images_list));
    numpy_images = [np.array(img) for img in images_list]
    fps = 30 
    # Duplicate each image to maintain the 1 second duration for each image
    numpy_images = [img for img in numpy_images for _ in range(fps * 4)]
    duration = len(images_list) * 4

    clip = ImageSequenceClip(numpy_images, fps=fps)
    clip = clip.set_duration(duration)

    if audio_data['audio_file_name']:
        audio_clip = AudioFileClip(audio_data['audio_file_path'])

        if audio_clip.duration < duration:
            pass
        else:
            audio_clip = audio_clip.subclip(0, duration)
        clip = clip.set_audio(audio_clip)
    
    temp_path = save_with_temp_file(clip, fps)    
    return temp_path


def convert_to_9_16_ratio(input_video, output_video):
    """
    Convert video to 9:16 aspect ratio (1080x1920 for Instagram)
    """
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
        temp_path = temp_file.name

        ffmpeg_path = 'ffmpeg'
        if not shutil.which('ffmpeg'):
            print("FFmpeg is not installed or not in PATH. Please install FFmpeg first.")
            ffmpeg_path = '/usr/bin/ffmpeg'
            
        command = [
            ffmpeg_path,
            '-y',
            '-i', input_video,
            '-vf', 'scale=1080:1920',
            '-c:a', 'copy',
            temp_path
        ]


        try:
            subprocess.run(command, check=True)
            # Move temp file to final output location
            os.replace(temp_path, output_video)
            print(f"Successfully converted video to 9:16 ratio: {output_video}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting video: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise
