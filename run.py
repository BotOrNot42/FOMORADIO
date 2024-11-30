"""
Main Module for the FomoRadio
"""
from datetime import datetime
from uuid import uuid4
import pytz
from src.utils.logger import custom_logger
from src.config import configuration as cf
from src.utils import json_loader, save_file, dir_checker
from src.activities import wait_for_next_show
from src.memory import MemoryClient
from src.data_collectors import TwitterClient
from src.script_generators import ScriptClient, LLMClient
from src.tts_transformers import TTSClient
from src.converters import mp3_to_mp4_converter


# Loading Configurations
radio_show = json_loader("./src/config/radio_show.json")
memory_config = json_loader("./src/config/memory_config.json")
configs = json_loader("./src/config/config.json")
rj_personas = json_loader("./src/config/rj_persona.json")


# Logger
logger = custom_logger(radio_show.get("radio_name"))
logger.info("Configurations loaded")
logger.info("Fomo Framework started")

# Create Logs and Media Directory
logger.info("Logger directory initialized")
dir_checker(cf.LOG_FOLDER)
logger.info("Media directory initialized")
dir_checker(cf.MEDIA_FOLDER)


# Loading Memory for personas
for each_persona in rj_personas:
    each_persona["memory"] = MemoryClient(memory_config)
    host_name = each_persona.get("host_name")
    logger.info("Memory Initialized for %s", host_name)

# Constants needed for the framework
EPISODE_COUNT = 1
RJ_INDEX = 0
WAIT_TIME = None
while True:
    # Collecting the data from multiple sources
    twitter_client = TwitterClient(
        cf.x_bearer_token, cf.x_radio_handle, cf.x_influencers
    )
    contents = twitter_client.process()
    logger.info("Got %d contents from %s", len(contents), twitter_client.source)
    if len(contents) == 0:
        logger.info("Trying different logic to fetch content")
        continue

    # Loading Contents to Personas
    memories = MemoryClient.content_to_memory(contents)
    for each_persona in rj_personas:
        each_persona["memory"].load_memory(memories)
        host_name = each_persona.get("host_name")
        logger.info("Memory Updated for %s", host_name)

    # Iterating through shows
    spoken_users = [i.get("user") for i in contents]
    for each_show in radio_show.get("shows"):
        # Loop iteration constant variables
        UNIQUE_ID = uuid4().hex[:8]
        WAIT_TIME = each_show.get("wait_time")
        # Filtering the RJs for that particular show
        filter_rjs = [
            i for i in rj_personas if i.get("show_id") == each_show.get("show_id")
        ]
        current_rj_index = RJ_INDEX % len(filter_rjs)
        next_rj_index = (RJ_INDEX + 1) % len(filter_rjs)
        # Generating the show script
        current_time = datetime.now(pytz.UTC).strftime("%I:%M %p UTC")
        script_client = ScriptClient(
            spoken_users,
            each_show,
            filter_rjs[current_rj_index],
            filter_rjs[next_rj_index].get("host_name"),
        )
        prompt = script_client.generate_prompt(twitter_client.source, current_time)
        llm_client, llm_interact = LLMClient(configs.get("llm")).initialize_client()
        generated_script = llm_interact(llm_client, prompt)
        current_rj_name = filter_rjs[current_rj_index].get("host_name")
        cleaned_response = generated_script.replace("\n", " ")
        logger.info("Script for %s - %s", current_rj_name, cleaned_response)
        # Generating the audio
        current_rj_voice = filter_rjs[current_rj_index].get("voice_id")
        tts_client, tts_interact = TTSClient(
            configs.get("tts"), cf.tts_api_key
        ).initialize_client()
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        radio_name = radio_show.get("radio_name").replace(" ", "")
        show_id = each_show.get("show_id")
        file_name = f"{cf.MEDIA_FOLDER}/{radio_name}-{show_id}-{UNIQUE_ID}-{timestamp}"
        audio_generator = tts_interact(tts_client, generated_script, current_rj_voice)
        is_audio_saved, audio_errors = save_file(audio_generator, f"{file_name}.mp3")
        if is_audio_saved:
            logger.info("Audio File saved as %s.mp3", file_name)
        else:
            logger.error("Generating audio file failed due to %s", audio_errors)
        # Generating video file
        show_details = (
            f"Funny Bunny Show | Host: {current_rj_name}  | "
            f"Episode: {EPISODE_COUNT} | {current_time}"
        )
        is_video_saved, video_errors = mp3_to_mp4_converter(
            configs.get("mp4"),
            f"{file_name}.mp3",
            f"{file_name}.mp4",
            cf.TEMP_VIDEO_FILE,
            show_details,
        )
        if is_video_saved:
            logger.info("Video File saved as %s.mp4", file_name)
        else:
            logger.error("Generating video file failed due to %s", video_errors)

        # Consuming the created media

        # Iterating through multiple rjs for a single show
        RJ_INDEX += 1
    wait_for_next_show(WAIT_TIME, logger)
