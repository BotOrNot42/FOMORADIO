#!/bin/bash

# Fomo Framework Environment Variables

### Data Collectors
# Twitter Account's bearer token to fetch the latest tweets
export x_bearer_token=""
# Twitter Account handle for the radio station. Should be without '@'.
export radio_handle=""
# Twitter Account handles of the influencers to watch for.
# Should be separated by commas without spaces and '@'.
export influencers=""
# Social Data API Key for fetching tweets
export social_data_api_key=""

### Script Generators
# OpenAI Key for summarizing the contents and generating new scripts
export OPENAI_API_KEY=""
# Text to Speech Module Key - By Default it points to Eleven Labs Key
export tts_api_key=""

### Consumers
## Twitter / X
# X API Key from the Twitter Developer App
export x_api_key=""
# X API Secret from the Twitter Developer App
export x_api_secret=""
# X Access Token for the radio station account after completing OAuth
export x_access_token=""
# X Access Token Secret for the radio station account after completing OAuth
export x_access_token_secret=""


echo "Environment variables successfully set"