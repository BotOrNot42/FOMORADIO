"""
Environment Configurations are loaded here :)
"""
import os

# Data Collection Environment Variables
x_bearer_token = os.environ.get("x_bearer_token")
x_radio_handle = os.environ.get("radio_handle")
x_influencers = os.environ.get("influencers").split(",")
social_data_api_key = os.environ.get("social_data_api_key")

# TTS Environment Variables
tts_api_key = os.environ.get("tts_api_key")

# Script Generator Environment Variables
llm_api_key = os.environ.get("llm_api_key")

# Folder Environment Variables
MEDIA_FOLDER = "media"
LOG_FOLDER = "logs"
TEMP_VIDEO_FILE = "media/temp_mp4.mp4"

# Consumer Environment Variables
x_api_key = os.environ.get("x_api_key")
x_api_secret = os.environ.get("x_api_secret")
x_access_token = os.environ.get("x_access_token")
x_access_token_secret = os.environ.get("x_access_token_secret")
