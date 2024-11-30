"""
Environment Configurations are loaded here :)
"""
import os

# Data Collection Environment Variables
x_bearer_token = os.environ.get("x_bearer_token")
x_radio_handle = os.environ.get("radio_handle")
x_influencers = os.environ.get("influencers")

# TTS Environment Variables
tts_api_key = os.environ.get("tts_api_key")

# Folder Environment Variables
media_folder = "media"
log_folder = "logs"
temp_video_file = "media/temp_mp4.mp4"