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
MEDIA_FOLDER = "media"
LOG_FOLDER = "logs"
TEMP_VIDEO_FILE = "media/temp_mp4.mp4"
